# tica_metadynamics
This git repo contains all the data + ipython notebooks necessary 
to reproduce the results in Sultan & Pande paper(JCTC 2017). The overarching 
idea is that we can use linear and non-linear kernel tica coordinates to enhance 
the sampling of regular MD trajectories via Metadyanmics. The nice thing being that 
we are dropping gaussians along the slowest set of CVs. In addition, with the landmark
kernel extension we are actually dropping guassians in full phase space if we use the 
RMSD distance metric. The data can then be used for qualitivative inspection of trajectories 
or combined into the MSM framework via TRAM/WHAM/MBAR etc. We also show that tica metadynamics 
can be extended to multiple orthogonoal coordinates by combining it a replica scheme(Bias-Exchange). 

Our numerical experiments have also shown that tica metandynamics can reversibly
drive transitions along the slowest modes even when NO such transition was seen 
in the tica training data. However, this does require information about the 
high and low free energy states and regular MD sampling to be performed in those 
basins. 

The paper is currently under second round of reviews, and since ACS is not amenable to 
pre-prints, this repo doesn't contain the actual paper document/pdf. 
 
The repo is organized into two folder sections. 
- Alanine 
- BPTI

Both sections contain a model(or several model folders),and a sub folder metad_data
which contains the results from running the metadynamics trajectories.The sections 
also contain a ipython notebook(in the ipynb folder) which contains all the scripts 
for making the figures as well as generating the plumed input files. We are currently 
creating a package that can hopefully automate the latter portion.  

Reproducing trajectories: 
To reproduce the enhanced sampling trajectories simply run ```python simulate.py```
in the appropriate ```metad_data```folder.The ```plumed.py``` file contains the 
actual plumed script that is added as an external force to OpenMM.In the case of BPTI, 
follow the instructions of the MPI connected replica exchange code code.  

Remaking Figures and re-generating plumed files:
The ipython notebooks contain all the necessary data scripts to make the figures shown in the paper.If 
you regenerate the trajectories then you will need to re-run `plumed sum_hills --hills HILLS` 
to integrate the FES to obtain a new fes.dat file.  

Notes:
- For BPTI, we are unable to provide the raw trajectories, featurizer objects, and landmark 
pdbs due to copy right issues. 
- The simulations are perfomed using openmm and plumed via the openmm plumed plugin. 
- Please ensure that you install plumed with libmatheval support. 

