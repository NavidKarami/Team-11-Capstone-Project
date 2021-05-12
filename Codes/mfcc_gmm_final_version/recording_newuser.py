import time as t
import pyaudio
import time
import wave
import numpy
import scipy.io.wavfile
from scipy.fftpack import dct
from SpeakerIdentification import *

def train_model(name):
    # We read 15 audio files for each used. Extract the features of each and save it in the features. 
	# We calculate the gmm of the features vector and store it
	# gmm is our database
    audio_num = 1
    #source = "%s_sample" %name+str(audio_num)+".wav"
    source = "%s_"%name+str(audio_num)+".wav"   
    dest = "trained_models/"
    train_file = "training_set.txt"        
    file_paths = open(train_file,'r')
    count = 1
    features = np.asarray(())	#convert the data into an array
    for path in file_paths:    
        path = path.strip()   
        print(path)

        sr,audio = read(path)
        print(sr)
        vector = extract_features(audio,sr)
	    
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
            #print('+ modeling completed for speaker:',picklefile," with data point = ",features.shape)
            print("Model created for user: %s" %name)   
            features = np.asarray(())
            count = 0
        count = count + 1
    #let's remove the contents of training_set.txt file and all the audio files
    # open file 
    f = open(train_file, "r+") 
    # absolute file positioning
    f.seek(0) 
    # to erase all data 
    f.truncate()
    f.close() 
    k = 1
    file_paths.close()
    for j in range(15):
        os.remove("%s_"%name+str(k)+".wav")
        k = k + 1
        
# Countdown function starts here
def stopwatch(sec):                 
    while sec:
        minn, secc = divmod(sec, 60)
        timeformat = '{:02d}:{:02d}'.format(minn, secc)
        print(timeformat, end='\r')
        t.sleep(1)
        sec -= 1
        
def record_audio_train(name):
    training = "training_set.txt"
    file = open(training, 'a')
    j = 0
    count = 1
    print("You will recored 15 audio files back to back for training purposes.")
    print("Please say the phrase into the microphone after a short delay with normal tone and speed")
    for j in range(15):    
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 512
        RECORD_SECONDS = 3
        device_index = 2
        audio = pyaudio.PyAudio()

        stopwatch(2)
        print ("recording started" + "Audio file #"+str(count))
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output = True, frames_per_buffer=CHUNK)
        Recordframes = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            Recordframes.append(data)
        print ("recording stopped")
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
