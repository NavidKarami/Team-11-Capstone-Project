import time as t
import pyaudio
import time
import wave

def stopwatch(sec):     		# Countdown function starts here, we pass a value to it to countdown from          
    while sec:
        minn, secc = divmod(sec, 60)	
        timeformat = '{:02d}:{:02d}'.format(minn, secc)
        print(timeformat, end='\r')	# print the time counting down
        t.sleep(1)
        sec -= 1
        
def record_audio_test():		# this function is used to start recording our audio file
    FORMAT = pyaudio.paInt16		# a bunch of variables we need to set 
    CHANNELS = 1
    RATE = 44100
    CHUNK = 512
    RECORD_SECONDS = 3
    device_index = 2
    audio = pyaudio.PyAudio()		
    
    print("Please say the phrase into the microphone after a short delay with normal tone and speed")
    stopwatch(2)			# call the stopwatch right before recording
    print ("Recording started")
    					
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
	
    waveFile = wave.open(OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(Recordframes))
    waveFile.close()
