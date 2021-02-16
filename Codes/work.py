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

def sound_fft(sound, rate):

    fs_rate, signal = wavfile.read("dn2.wav")

    n = len(sound)  #How long is the file
    T = 1/rate      #Sampling interval in time

    fft = scipy.fft.fft(sound)   # Do FFT
    fft = abs(fft)    #Get rid of the imaginary part

    print(fft[393])
    fft = np.array(fft)

    #Find the highest peak and print it
    peaks,_ = find_peaks(fft, distance=30, height=10) #Find the peaks (peaks > 10)
    peak1 = np.argmax(fft)
    print("Highest Peak is: ", peak1)

    xf = np.linspace(0.0, 1.0/(2.0*T), int(n/2))
    #xf = np.linspace(0.0, T*rate, int(n/2))
    one_side = np.abs(fft[:n//2])
    #print(one_side)
    """
    fig, ax = plt.subplots()
    #ax.plot(xf, 2.0/n * one_side) #Small magnitude
    ax.plot(xf, one_side) #Make magnitude larger
    #ax.plot(xf, np.abs(yf[:n//2]))
    """
    #plt.plot(one_side) #plot one side of the FFT

    plt.plot(one_side)
    plt.plot(peaks, fft[peaks], "x")
    plt.grid()
    plt.xlabel("Frequency")
    plt.ylabel("Magnitude")
    plt.show()

    #return plt.show()

def main():
    file_path = "dn2.wav"
    samples, sampling_rate = librosa.load(file_path, sr = None, mono = True, offset = 0.0, duration = None)
    sound_fft(samples, sampling_rate)

if __name__ == '__main__':
    main()