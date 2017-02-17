from msmbuilder.utils import load,dump
from msmbuilder.featurizer import DihedralFeaturizer
import os, glob
from msmbuilder.decomposition import tICA
import mdtraj as md 
import pandas as pd 
from msmbuilder.msm import MarkovStateModel
from msmbuilder.cluster import KMeans


trj_list = load("traj_list.pkl")
print("Found %d trajs"%len(trj_list))

f=DihedralFeaturizer(sincos=False)
dump(f,"raw_featurizer.pkl")

feat = f.transform(trj_list)

dump(feat, "raw_features.pkl")


f=DihedralFeaturizer()
dump(f,"featurizer.pkl")
df1 = pd.DataFrame(f.describe_features(trj_list[0]))
dump(df1,"feature_descriptor.pkl")
feat = f.transform(trj_list)

dump(feat, "features.pkl")


t = tICA(lag_time=100,n_components=1,kinetic_mapping=False)

tica_feat = t.fit_transform(feat)

dump(t,"tica_mdl.pkl")
dump(tica_feat,"tica_features.pkl")

kmeans_mdl = KMeans(50)
ass=kmeans_mdl.fit_predict(tica_feat)
msm_mdl = MarkovStateModel(100)
msm_mdl.fit(ass)


dump(kmeans_mdl,"kmeans_mdl.pkl")
dump(ass,"assignments.pkl")
dump(msm_mdl, "msm_mdl.pkl")
