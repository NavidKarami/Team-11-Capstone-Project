import os
import wave
import time
import pickle
import time as t
import pyaudio
import warnings
import numpy as np
from sklearn import preprocessing
from scipy.io.wavfile import read
import python_speech_features as mfcc
from sklearn.mixture import GaussianMixture 

warnings.filterwarnings("ignore")

def calculate_delta(array):
   
    rows,cols = array.shape
    #print(rows)
    #print(cols)
    deltas = np.zeros((rows,20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i-j < 0:
              first =0
            else:
              first = i-j
            if i+j > rows-1:
                second = rows-1
            else:
                second = i+j 
            index.append((second,first))
            j+=1
        deltas[i] = ( array[index[0][0]]-array[index[0][1]] + (2 * (array[index[1][0]]-array[index[1][1]])) ) / 10
    return deltas

def extract_features(audio,rate):
       
    mfcc_feature = mfcc.mfcc(audio,rate, 0.025, 0.01,20,nfft = 1200, appendEnergy = True)    
    mfcc_feature = preprocessing.scale(mfcc_feature)
    #print(mfcc_feature)
    delta = calculate_delta(mfcc_feature)
    combined = np.hstack((mfcc_feature,delta)) 
    return combined

def test_model(name):
	flag = False
	source = "sample.wav"
	modelpath = "trained_models/"
	 
	gmm_files = [os.path.join(modelpath,fname) for fname in
	              os.listdir(modelpath) if fname.endswith('.gmm')]
	 
	#Load the Gaussian gender Models
	models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]
	speakers   = [fname.split("\\")[-1].split(".gmm")[0] for fname 
	              in gmm_files]
	 
	# Read the test directory and get the list of test audio files 

	sr,audio = read(source)
	vector   = extract_features(audio,sr)
	log_likelihood = np.zeros(len(models)) 

	for i in range(len(models)):
		gmm = models[i]  #checking with each model one by one
		scores = np.array(gmm.score(vector))
		log_likelihood[i] = scores.sum()
	
	name_compare = "trained_models/%s_15.wav" %name
	#print(name_compare)
	winner = np.argmax(log_likelihood)
	if str(speakers[winner]) == str(name_compare):
			print("Okay good %s" %name)
			flag = True
			os.remove("sample.wav")
			time.sleep(1.0)
			return flag
	#print("\tdetected as - ", speakers[winner])
	else:
		print("failed")
		flag = False
		return flag