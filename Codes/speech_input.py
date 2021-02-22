import speech_recognition as sr
import os 
import sys
import math
import array
import librosa
from librosa import display
from matplotlib import pyplot as plt 
import scipy
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_prominences
import numpy as np
from peakdetect import peakdetect
from numpy import NaN, Inf, arange, isscalar, asarray, array
from collections import OrderedDict
from scipy.signal import argrelextrema
from scipy.signal import argrelmax
import scipy.io.wavfile as wavfile
from scipy.io.wavfile import write

MicrophoneInstance = sr.Recognizer() #creates recognizer instance, library settings etc
mic = sr.Microphone() #access default system microphone, create microphone instance
with mic as source:
    MicrophoneInstance.adjust_for_ambient_noise(source) #calibrates microphone to adjust for noise
    print("say a phrase") #message asking the user to say something
    audio = MicrophoneInstance.listen(source) #capture audio input until silence is detected
    with open('user_input_speech.wav', 'wb') as f: # writes the audio data onto the wav file
        f.write(audio.get_wav_data()) 


samples, sampling_rate = librosa.load('user_input_speech.wav', sr = None, mono = True, offset = 0.0, duration = None)
n = len(samples)
fft = scipy.fft.fft(samples)
fft = abs(fft)
fft = np.array(fft)
fft_one_side = np.abs(fft[:n//2])
peaks,_ = find_peaks(fft_one_side, distance=80, height=10) #Got rid of the unwanted X
one_side = np.abs(fft[:n//2])
plt.plot(one_side)
plt.plot(peaks, fft[peaks], "x")
plt.grid()
plt.xlabel("Frequency")
plt.ylabel("Magnitude")
plt.show()