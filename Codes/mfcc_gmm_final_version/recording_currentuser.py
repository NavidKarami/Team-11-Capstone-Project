import time as t
import pyaudio
import time
import wave

def stopwatch(sec):     		# Countdown function starts here, we pass a value to it to countdown from in sec          
    while sec:
        minn, secc = divmod(sec, 60)	
        timeformat = '{:02d}:{:02d}'.format(minn, secc)
        print(timeformat, end='\r')	# print the time counting down
        t.sleep(1)
        sec -= 1
        
def record_audio_test():		# this function is used to start recording our audio file
    FORMAT = pyaudio.paInt16		# 16-bit integer 
    CHANNELS = 1			# 1 is for mono, change to 2 if you want stereo
    RATE = 44100			# 44100 samples per second. Standard value for when performing audio recording for human 
    CHUNK = 512				# number of frames the signals are split into
    RECORD_SECONDS = 3			# Record 3 seconds			
    audio = pyaudio.PyAudio()		# create a variable audio to set the PyAudio class variables prior to recording 
    
    print("Please say the phrase into the microphone after a short delay with normal tone and speed")
    stopwatch(2)			# call the stopwatch right before recording
    print ("Recording started")
    #set the PyAudio class variables 					
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output = True, frames_per_buffer=CHUNK)
    Recordframes = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        Recordframes.append(data)
    print ("recording stopped")
    stream.stop_stream()		# stop recording and turn off the mic
    stream.close()
    audio.terminate()
    OUTPUT_FILENAME="sample.wav"	# we name the recording sample.wav
    #Open the audio files and set the parameters 		
    waveFile = wave.open(OUTPUT_FILENAME, 'wb')		 # open the audio file as write only mode
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT)) # Set the sample width to n bytes
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(Recordframes))	# Write audio frames and make sure nframes(512) is correct
    waveFile.close()					# close our audio file
