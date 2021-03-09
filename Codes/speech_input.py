import speech_recognition as sr #library that allows to access system's default microphone and use for input. install with pip install SpeechRecognition
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

def main():
    # MicrophoneInstance = sr.Recognizer() #creates recognizer instance, library settings etc
    # mic = sr.Microphone() #access default system microphone, create microphone instance
    # with mic as source:
    #     MicrophoneInstance.adjust_for_ambient_noise(source) #calibrates microphone to adjust for noise
    #     print("say a phrase") #message asking the user to say something
    #     audio = MicrophoneInstance.listen(source) #capture audio input until silence is detected
    #     with open('danny13.wav', 'wb') as f: # writes the audio data onto the wav file
    #         f.write(audio.get_wav_data())


    #below code in fft_vx.x code. used for testing to assure input file worked
    samples, sampling_rate = librosa.load('n3.wav', sr = None, mono = True, offset = 0.0, duration = None)
    n = len(samples)
    fft = scipy.fft.fft(samples)
    fft = abs(fft)
    fft = np.array(fft)
    fft_one_side = np.abs(fft[:n//2])
    peaks,_ = find_peaks(fft_one_side, distance=60, height=10) #Got rid of the unwanted X
    peak_mags = fft[peaks]
    peak_freq_and_mags = np.vstack((peaks,peak_mags))
    np.savetxt('n3.txt', peak_freq_and_mags, fmt='%1.2f', header='sampled data\nphrase said\n"this is danny"\nfrequency\nmagnitude', comments='# ')
    # # print(peaks)
    # # print(fft[peaks])
    # # print(peak_mags)
    # # print(peak_freq_and_mags)
    # # print(peak_freq_and_mags[1])
    one_side = np.abs(fft[:n//2])
    plt.plot(one_side)
    plt.plot(peaks, fft[peaks], "x")
    plt.grid()
    plt.xlabel("Frequency")
    plt.ylabel("Magnitude")
    plt.show()

if __name__ == '__main__':
    main()
