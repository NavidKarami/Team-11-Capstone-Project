import time as t
import pyaudio
import time
import wave
import numpy
import scipy.io.wavfile
from scipy.fftpack import dct
from voice_authentication import *

def train_model(name):			# pass the username we are logging in as
    # We read 15 audio files for each user. Extract the features of each and save it in the features. 
    # We calculate the gmm of the features vector and store it in the trained models folder
    audio_num = 1
    source = "%s_"%name+str(audio_num)+".wav"   
    dest = "trained_models/"			# save the location of the models into dest
    train_file = "training_set.txt"        	# name of training audio files to be read
    file_paths = open(train_file,'r')		# open the text file
    count = 1
    features = np.asarray(())	# convert the data into an array
    for path in file_paths:    	# read all the audio files
        path = path.strip()   	# get rid of .wav of audio file names

        sr,audio = read(path)				# get the signal data and sample rate 
        vector = extract_features(audio,sr) 		# extract the audio file features with mfcc + delta approach
	    						
        if features.size == 0:				# check if there were any features collected or no
            features = vector				# We are making sure not to duplicate data into our features array
        else:
            features = np.vstack((features, vector))	# add all the 15 audio files features into one single array

        if count == 15:    				# if all 15 audio files read and processed, start creating the model
            gmm = GaussianMixture(n_components = 6, max_iter = 200, covariance_type='diag',n_init = 3)	# define your gaussian mixture model params
            gmm.fit(features)										# draw the best fit line throught it
	        
	    # dumping the trained gaussian model
            picklefile = path.split("-")[0]+".gmm"
            pickle.dump(gmm,open(dest + picklefile,'wb'))	# open the destination
            print("Model created for user: %s" %name)   	# save it in the destination folder
            features = np.asarray(())				# reset features array values for the next run
            count = 0					# reset count to 0
        count = count + 1				# there are still more audio files to read, increment count and read the next one
	
    # let's remove the contents of training_set.txt file and all the audio files
    f = open(train_file, "r+") 		# open file 
    f.seek(0) 				# absolute file positioning
    f.truncate()		    	# to erase all data 
    f.close() 				# close the file
    k = 1
    file_paths.close()
    for j in range(15):			# remove all the 15 audio files
        os.remove("%s_"%name+str(k)+".wav")
        k = k + 1
        
# Countdown function starts here, previously defined in other module
def stopwatch(sec):                 
    while sec:
        minn, secc = divmod(sec, 60)
        timeformat = '{:02d}:{:02d}'.format(minn, secc)
        print(timeformat, end='\r')
        t.sleep(1)
        sec -= 1
        
def record_audio_train(name):		# pass username to our function which is for recording 15 audio files
    training = "training_set.txt"	# load the training set text file
    file = open(training, 'a')		
    j = 0
    count = 1
    print("You will recored 15 audio files back to back for training purposes.")
    #print("Please say 'this is (name)' into the microphone after a short delay with normal tone and speed")
    print("Please say the phrase 'this is (your name)' into the microphone after a 2 second delay")
    for j in range(15):    
        FORMAT = pyaudio.paInt16	# see recording_currentuser for comments on this (same process/variables)
        CHANNELS = 1
        RATE = 44100
        CHUNK = 512
        RECORD_SECONDS = 3
        device_index = 2
        audio = pyaudio.PyAudio()

        stopwatch(2)
        print ("Recording started" + " Audio file #"+str(count))
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output = True, frames_per_buffer=CHUNK)
        Recordframes = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            Recordframes.append(data)
        print ("Recording stopped")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        OUTPUT_FILENAME= name+"_"+str(count)+".wav"
        waveFile = wave.open(OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(Recordframes))
        waveFile.close()
        print(OUTPUT_FILENAME+" created")
        count = count + 1
        file.write(OUTPUT_FILENAME+"\n")
        
    file.close()
