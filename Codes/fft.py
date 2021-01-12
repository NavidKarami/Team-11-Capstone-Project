import os 
import librosa
from librosa import display
from matplotlib import pyplot as plt 
#import numba

file_path = "Recording.wav"
samples, sampling_rate = librosa.load(file_path, sr = None, mono = True, offset = 0.0, duration = None)

len(samples), sampling_rate
l = len(samples)
r = sampling_rate

print("Number of samples is: %d" %l)     # Number of samples
print("Number of samples per second is: %d " %r)    # We were capturing X amplitudes every second

duration = len(samples)/sampling_rate   # How long was the audio
print("Audio file was %.2f seconds long" %(duration))

plt.figure()
librosa.display.waveplot( y = samples, sr = sampling_rate)
plt.xlabel("Time (seconds) -->")
plt.ylabel("Amplitude")
plt.show()
