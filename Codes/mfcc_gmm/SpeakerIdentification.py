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
        

def train_model(name):
	# We read 15 audio files for each used. Extract the features of each and save it in the features. 
	# We calculate the gmm of the features vector and store it
	# gmm is our database 
	source   = "training_set/"   
	dest = "trained/"
	train_file = "training_set_addition.txt"        
	file_paths = open(train_file,'r')
	count = 1
	features = np.asarray(())	#convert the data into an array
	for path in file_paths:    
	    path = path.strip()   
	    print(path)

	    sr,audio = read(source + path)
	    print(sr)
	    vector   = extract_features(audio,sr)
	    
	    if features.size == 0:
	        features = vector
	    else:
	        features = np.vstack((features, vector))

	    if count == 15:    
	        gmm = GaussianMixture(n_components = 6, max_iter = 200, covariance_type='diag',n_init = 3)
	        gmm.fit(features)
	        
	        # dumping the trained gaussian model
	        picklefile = path.split("-")[0]+".gmm"
	        pickle.dump(gmm,open(dest + picklefile,'wb'))
	        print('+ modeling completed for speaker:',picklefile," with data point = ",features.shape)   
	        features = np.asarray(())
	        count = 0
	    count = count + 1

def test_model(name):
	flag = 0
	source   = "sample.wav"  
	modelpath = "trained_models/"       
	file_paths = open(source,'r')
	 
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
	    gmm    = models[i]  #checking with each model one by one
	    scores = np.array(gmm.score(vector))
	    log_likelihood[i] = scores.sum()
	
	name_compare = "trained_models/%s_15.wav" %name
	winner = np.argmax(log_likelihood)
	score_compare = log_likelihood[winner]
	if speakers[winner] == name_compare:
		print("Welcome", name)
		flag = 1
		time.sleep(1.0)
		file_paths.close()
		return flag
	else:
		flag = 0
		print("Failed")
		file_paths.close()
		return flag