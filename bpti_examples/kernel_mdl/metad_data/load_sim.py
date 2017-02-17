import os
from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
from msmbuilder.io import backup
from openmmplumed import PlumedForce

def serializeObject(obj,objname):
    objfile = open(objname,'w')
    objfile.write(XmlSerializer.serialize(obj))
    objfile.close()


def create_simulation(base_dir, tic_index,plumed_script):
    print("Creating simulation for tic %d"%tic_index)
    starting_dir = os.path.join(base_dir, "starting_coordinates")
    os.chdir((os.path.join(base_dir,"tic_%d"%tic_index)))

    if os.path.isfile("./state.xml"):
        state = XmlSerializer.deserialize(open("./state.xml").read())
    else:
        state = XmlSerializer.deserialize(open("%s/state0.xml"%starting_dir).read())


    system =  XmlSerializer.deserialize(open("%s/system.xml"%starting_dir).read())
    integrator = XmlSerializer.deserialize(open("%s/integrator.xml"%starting_dir).read())
    pdb = app.PDBFile("%s/0.pdb"%starting_dir)

    new_f = PlumedForce(plumed_script)
    new_f.setForceGroup(1)
    system.addForce(new_f)

    platform = Platform.getPlatformByName("CUDA")
    properties = {'CudaPrecision': 'mixed', 'CudaDeviceIndex': str(tic_index)}
    simulation = app.Simulation(pdb.topology, system, integrator, platform, properties)
    if os.path.isfile("./checkpt.chk"):
        with open("checkpt.chk",'rb') as f:
            simulation.context.loadCheckpoint(f.read())
    else:
        simulation.context.setState(state)
    print("Done creating simulation for tic %d"%tic_index)

    f = open("./speed_report.txt",'w')
    backup("trajectory.dcd")
    simulation.reporters.append(app.DCDReporter('trajectory.dcd', 100000))
    simulation.reporters.append(app.StateDataReporter(f, 1000, step=True,\
                                potentialEnergy=True, temperature=True, progress=True, remainingTime=True,\
                                speed=True, totalSteps=200*100, separator='\t'))


    return simulation


def run_simulation(simulation, n_steps):
    os.path.chdir(base_dir,"tic_%d"%tic_index)
    simulation.step(n_steps)
    backup("state.xml")
    state=simulation.context.getState(getPositions=True, getVelocities=True,\
    getForces=True,getEnergy=True,getParameters=True,enforcePeriodicBox=True)
    serializeObject(state,'state.xml')
    return simulation

def backup_simulation(simulation, tic_index):
    return
    #backup()
     # s = simulation.context.getState(getEnergy=True,groups={1})
     #
     # energy_1 = s.getPotentialEnergy().value_in_unit(kilojoule_per_mole)




