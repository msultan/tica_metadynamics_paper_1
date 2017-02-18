from msmbuilder.utils import load,dump
from msmbuilder.featurizer import DihedralFeaturizer,LandMarkRMSDFeaturizer
import os, glob
from msmbuilder.decomposition import tICA
import mdtraj as md 
import pandas as pd 
from msmbuilder.msm import MarkovStateModel
from msmbuilder.msm.validation import BootStrapMarkovStateModel
from msmbuilder.cluster import KMeans

flist = glob.glob("./run*.xtc")

top = md.load("../top.pdb")
trj_list = [md.load(i,top=top) for i in flist]
print("Found %d trajs"%len(trj_list))

f=DihedralFeaturizer(sincos=False)
dump(f,"raw_featurizer.pkl")

feat = f.transform(trj_list)

dump(feat, "raw_features.pkl")


f = load("../featurizer.pkl")
df1 = pd.DataFrame(f.describe_features(trj_list[0]))
dump(df1,"feature_descriptor.pkl")
feat = f.transform(trj_list)

dump(feat, "features.pkl")


t = load("../tica_mdl.pkl")
t.commute_mapping =  False
tica_feat = t.transform(feat)
dump(t, "tica_mdl.pkl")
dump(tica_feat,"tica_features.pkl")

kmeans_mdl = load("../kmeans_mdl.pkl")
ass=kmeans_mdl.predict(tica_feat)

#these trjaectories are saved at 200ps instead of 20ps
msm_mdl = load("../msm_mdl.pkl")
msm_mdl.lag_time=5
msm_mdl.fit(ass)

dump(kmeans_mdl,"kmeans_mdl.pkl")
dump(ass,"assignments.pkl")
dump(msm_mdl, "msm_mdl.pkl")
