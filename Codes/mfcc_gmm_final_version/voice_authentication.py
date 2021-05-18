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

# This functiona extract the audio file features - the features are called Mel-frequency Cepstral Coefficients (MFCCs)
def extract_features(audio,rate):		
    mfcc_feature = mfcc.mfcc(audio,rate, 0.025, 0.01,20,nfft = 1200, appendEnergy = True)
#Here we are performing Standardization of datasets
#In practice we often ignore the shape of the distribution and just transform the data to center it by removing the mean value of each feature, then scale it by dividing non-constant features by their standard deviation.
    mfcc_feature = preprocessing.scale(mfcc_feature)
#The MFCC feature vector describes only the power spectral envelope of a single frame
# we also want have information in the dynamics - what are the trajectories of the MFCC coefficients over time so we calculate the derivative 	
# If we have 12 MFCC coefficients, we would also get 12 delta coefficients, which would combine to give a feature vector of length 24.
    delta = calculate_delta(mfcc_feature)
    combined = np.hstack((mfcc_feature,delta)) # Combining the mfcc coefs with deltas 
    return combined

def test_model(name):				# we are passing the username to this function
	flag = False				# setting flag as false and loading the freshly recorded audio file and trained models folder
	source = "sample.wav"
	modelpath = "trained_models/"
	gmm_files = [os.path.join(modelpath,fname) for fname in
	              os.listdir(modelpath) if fname.endswith('.gmm')]
	 
	#Load the Gaussian gender Models
	models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]
	speakers   = [fname.split("\\")[-1].split(".gmm")[0] for fname 
	              in gmm_files]
	 
	# Read the sample.wav audio file and extract its features  
	sr,audio = read(source)
	vector   = extract_features(audio,sr)
	log_likelihood = np.zeros(len(models)) 

	for i in range(len(models)):
		gmm = models[i]  		# checking with each model one by one
		scores = np.array(gmm.score(vector))
		log_likelihood[i] = scores.sum()
	
	name_compare = "trained_models/%s_15.wav" %name
	winner = np.argmax(log_likelihood)
	if str(speakers[winner]) == str(name_compare):	# if the user matches the gmm files of the user you're trying to enter as then you proceed			
			print("Voice authentication complete for %s" %name)
			flag = True		# set flag to true
			os.remove("sample.wav")	# deleting the fresh audio file
			time.sleep(1.0)
			return flag		# returning the flag to the code where this function was called
	else:					
		print("Failed authentication for %s" %name)	# if you dont match then you get a error message and the flag is set as false
		os.remove("sample.wav")
		flag = False
		return flag
