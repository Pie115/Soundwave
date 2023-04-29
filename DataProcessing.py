from encodec import EncodecModel
from encodec.utils import convert_audio
import torchaudio
import torch
from sklearn.decomposition import PCA
import pickle as pk
from glob import glob
import torch
from torch.distributions import constraints
import pyro
import pyro.distributions as dist
from pyro.infer import SVI, Trace_ELBO
import matplotlib.pyplot as plt

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

def stackWavs(wavs): # A List of WAV Files
  return torch.stack([convert_audio(wav, sr, model.sample_rate, model.channels)[: ,:1697750]  for wav in wavs])

def processAudio(wavs): # Return a Tensor (N, Z) of latent encodings
  return getZ(stackWavs(wavs))

def CreatePCA(Data): # FED A PROCESSED LATENT VECTOR
  N, D = Data.shape
  pca = PCA(n_components=min(N, 128)).fit(allData)
  pk.dump(pca, open("pca.pkl","wb"))

def GetPCA(): # FED A PROCESSED LATENT VECTOR
  pca_reload = pk.load(open("pca.pkl",'rb'))
  return pca_reload

def CreatePCAEmbeddings(data): # CREATE PCA EMBEDDINGS GIVEN LATENT VECTOR
  pca = GetPCA()
  return pca.transform(data)

def trainMVN(data):
  steps = 10000
  N, Z = data.shape

  mean = torch.zeros(Z, requires_grad=True)
  cov = torch.eye(Z, requires_grad=True)

  optimizer = torch.optim.Adam([mean, cov], lr=1e-2)

  for step in range(steps+1):
    
    m = dist.MultivariateNormal(mean, cov)
    optimizer.zero_grad()
    loss = -m.log_prob(data).mean()
    loss.backward()
    optimizer.step()
    #m.clear_cache()
    if step % 50 == 0:
      print('step: {}, loss: {}'.format(step, loss.item()))


  return dist.MultivariateNormal(mean, cov)