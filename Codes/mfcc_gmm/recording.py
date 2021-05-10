
import time as t
import pyaudio
import time
import wave

def stopwatch(sec):                 # Countdown function starts here
    while sec:
        minn, secc = divmod(sec, 60)
        timeformat = '{:02d}:{:02d}'.format(minn, secc)
        print(timeformat, end='\r')
        t.sleep(1)
        sec -= 1
        
def record_audio_test():
    
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 512
    RECORD_SECONDS = 3
    device_index = 2
    audio = pyaudio.PyAudio()
    
    print("Please say the phrase into the microphone after a short delay with normal tone and speed")
    stopwatch(2)
    print ("recording started")
    
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output = True, frames_per_buffer=CHUNK)
    Recordframes = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        Recordframes.append(data)
    print ("recording stopped")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    OUTPUT_FILENAME="sample.wav"
	
    waveFile = wave.open(OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(Recordframes))
    waveFile.close()