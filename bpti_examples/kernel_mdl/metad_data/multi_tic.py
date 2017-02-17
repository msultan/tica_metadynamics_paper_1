#!/bin/env python

from load_sim import create_simulation
from mpi4py import MPI
import numpy as np
from simtk.unit import *

import sys,os
from plumed import *

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

sim_temp = 300
beta = 0.0083144621 * 300


base_dir = os.path.getcwd()

sim_obj = create_simulation(base_dir, rank ,globals()["plumed_%d"%rank]) 
for step in range(10000):
    print(step)
    #2fs *3000 =6ps
    sim_obj.step(3000)
    #get old energy for just the plumed force
    old_energy = sim_obj.context.getState(getEnergy=True,groups={1}).getPotentialEnergy().value_in_unit(kilojoule_per_mole)
    #write the chckpt
    with open("checkpt.chk",'wb') as f:
        f.write(sim_obj.context.createCheckpoint())
    #old_state=sim_obj.context.getState(getPositions=True, getVelocities=True,\
    #getForces=True,getEnergy=True,getParameters=True,enforcePeriodicBox=True)
    old_state = os.path.abspath("checkpt.chk")
    #send state and energy
    data = comm.gather((old_state,old_energy), root=0)

    if rank==0:
        #rnd pick 2 states
        i,j =  np.random.choice(np.arange(size), 2, replace=False)
        s_i_i,e_i_i = data[i]
        s_j_j,e_j_j = data[j]
        #swap out states
        data[j], data[i] = data[i],data[j]
    else:
        data = None

    #get possible new state
    new_state = None 
    new_state,energy = comm.scatter(data,root=0)
    #set state 
    with open(new_state, 'rb') as f:
        sim_obj.context.loadCheckpoint(f.read())

    #sim_obj.context.setState(new_state)

    # return new state and new energies 
    new_energy = sim_obj.context.getState(getEnergy=True,groups={1}).getPotentialEnergy().value_in_unit(kilojoule_per_mole)
    data = comm.gather((new_state,new_energy), root=0)

    if rank==0:
        s_i_j, e_i_j = data[i]
        s_j_i, e_j_i = data[j]
        print(e_i_i,e_j_j,e_i_j,e_j_i,np.min((1,np.exp(beta*(e_i_i+e_j_j - e_i_j - e_j_i)))))
        if np.random.rand() < np.min((1,np.exp(beta*(e_i_i+e_j_j - e_i_j - e_j_i)))):
            #do nothing and go forward
            print("Swapping out %d with %d"%(i,j),flush=True)
        else:
            print("Failed Swap of %d with %d"%(i,j),flush=True)
            #go back to original state list
            data[i], data[j] = data[j] , data[i]
    else:
        data = None

    #get final state for iteration
    new_state,energy = comm.scatter(data,root=0)
    #print(rank,new_state)
    with open(new_state, 'rb') as f:
        sim_obj.context.loadCheckpoint(f.read())

    #wait for everyone to catch up
    comm.barrier()
comm.barrier()
sys.exit()
