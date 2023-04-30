from pyro.distributions import diag_normal_mixture
from encodec import EncodecModel
from encodec.utils import convert_audio
import torchaudio
import torch
from sklearn.decomposition import PCA
import pickle as pk
import pandas as pd
from glob import glob
import os
import numpy as np
import torch
from torch.distributions import constraints
import pyro
import pyro.distributions as dist
from pyro.infer import SVI, Trace_ELBO
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
import sklearn.mixture as mix

from sklearn.neighbors import NearestNeighbors

# Instantiate a pretrained EnCodec model
model = EncodecModel.encodec_model_48khz()

TARGET_HERTZ = 6.0


model.set_target_bandwidth(TARGET_HERTZ)

def getZ(wav, sr = 48000): # FILE, SourceRate(Hz)
  with torch.no_grad():
      encoded_frames = model.encode(wav)
  codes = torch.cat([encoded[0] for encoded in encoded_frames], dim=-1)  # [B, n_q, T]

  B, T, C = codes.shape
  return codes.view(B, T*C)

def stackWavs(wavs, sr = 48000): # A List of WAV Files
  return torch.stack([convert_audio(wav, sr, model.sample_rate, model.channels)[: ,:1697750]  for wav in wavs])

def processAudio(wavs, sr = 48000): # Return a Tensor (N, Z) of latent encodings
  return getZ(stackWavs(wavs, sr))

def CreatePCA(Data): # FED A PROCESSED LATENT VECTOR
  N, D = Data.shape
  pca = PCA(n_components=min(N, 64)).fit(Data)
  pk.dump(pca, open("pca.pkl","wb"))


def GetPCA(): # FED A PROCESSED LATENT VECTOR
  pca_reload = pk.load(open("pca.pkl",'rb'))
  return pca_reload


def CreatePCAEmbeddings(data): # CREATE PCA EMBEDDINGS GIVEN LATENT VECTOR
  pca = GetPCA()
  return pca.transform(data)


def createZTable(files, PCA = False, nm = None): # GIVEN A SET OF FILES CREATE THE Z TABLE
  Data = []

  for file in files:
    wav, sr = torchaudio.load(file)
    Data += [wav] # STACK IT ON CLASS DATA

  Data = processAudio(Data, sr) # PROCESS ALL DATA (B, n_q, EmbedDim)

  if PCA == True:
    CreatePCA(Data)
    
  Data = CreatePCAEmbeddings(Data)
  

  tab = {os.path.basename(f)[:-4]:d for f, d in zip(files, Data)}

  if nm == None:
    pk.dump(tab, open("songData.pkl","wb"))
  else:
    pk.dump(tab, open(nm, "wb"))

  return tab


def loadZTable(): # LOADS THE Z TABLE GIVEN THAT IT EXISTS
  tab  = pk.load(open("songData.pkl",'rb'))
  tab.update(pk.load(open("songDataRap.pkl",'rb')))
  return tab

def trainMVN(data):
    
    X = np.stack(list(loadZTable().values()), axis = 0)
    
    neigh = NearestNeighbors(n_neighbors = 5, n_jobs = 1)
    
    neigh.fit(X)
    
    dist, ind = neigh.kneighbors(X)
    
    return ind

    #X = X[ind.ravel()]
    
    #return mix.GaussianMixture(n_components = 3).fit(X)

def queryMaximumLikelihood(songs):

  tab = loadZTable()

  zs = []

  for s in songs:
    if s in tab.keys():
      zs += [tab[s]]

  zs = torch.stack([torch.Tensor(z) for z in zs], axis = 0)

  ind = trainMVN(zs)
 
  #songs = [(i, g.predict(torch.Tensor(j).unsqueeze(0)) ) for i, j in tab.items()]
    
  
  songs = list(tab.keys())
    
  songs = [[songs[i] for i in z] for z in ind]
    
  #songs.sort(key = lambda x : x[1])

  return songs
