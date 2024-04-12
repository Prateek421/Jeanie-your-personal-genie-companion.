import librosa.feature as lf
import librosa
import numpy as np

def zcr(data,frame_length,hop_length):
    zcr=librosa.feature.zero_crossing_rate(data,frame_length=frame_length,hop_length=hop_length)
    return np.squeeze(zcr)

def rmse(data,frame_length=2048,hop_length=512):
    #rmse=librosa.feature.rms(y=data)
    rmse=np.sqrt(np.mean(np.square(data)))
    return np.squeeze(rmse)

def mfccc(data,sr,frame_length=2048,hop_length=512,flatten:bool=True):
    mfcc=lf.mfcc(y=data,sr=sr)
    return np.squeeze(mfcc.T)if not flatten else np.ravel(mfcc.T)

def extract_features(data,sr,frame_length=2048,hop_length=512):
    result=np.array([])
    
    result=np.hstack((result,
                      zcr(data,frame_length,hop_length),
                      rmse(data,frame_length,hop_length),
                      mfccc(data,sr,frame_length,hop_length)
                     ))
    return result