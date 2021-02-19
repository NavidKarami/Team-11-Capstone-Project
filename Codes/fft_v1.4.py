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

#This function can find the magnitude of the peaks
def peak_finder(peaks, fft, length):
#init the arrays
    h = []
    q = []   
    for k in range (0, length):
        q[k] = q.append(0)  # Add bunch of 0s
        h[k] = h.append(0)  # Add bunch of 0s. This is init array

#find the magnitude of the peaks
    for i in range (0, len(peaks)): #loop through peaks and find the highest
        q[i] = fft[peaks[i]]
        h[i] = q[i]                  
#sort the magnitudes 
    q.sort(reverse = True)
    a = q[0] #Mag of the 1st highest peak
    print("In peak_finder function Mag of the 1st highest peak is:", a)

def sound_fft(sound, rate):

    fs_rate, signal = wavfile.read("dn2.wav")   # do not worry about this. 

    n = len(sound)  #How long is the audio file
    T = 1/rate      #Sampling interval in time

    fft = scipy.fft.fft(sound)   #Do FFT
    fft = abs(fft)    #Get rid of the imaginary part
    #print(fft[393])
    fft = np.array(fft) #Performing FFT. We could use scipy library too

    #Find the highest peak and print it
    fft_one_side = np.abs(fft[:n//2])
    #peaks,_ = find_peaks(fft, distance=80, height=10) #Find the peaks (peaks > 10)
    peaks,_ = find_peaks(fft_one_side, distance=80, height=10) #Got rid of the unwanted X
    peak1 = np.argmax(fft)
   
    print("Highest Peak is:", peak1)
    print("The highest peak magnitude is:", fft[peak1])
   
    length = len(peaks)
    peak_finder(peaks, fft, length)

    #This is a test
    prominences = peak_prominences(fft, peaks, wlen=25)[0]
    #print(prominences)
    #print(fft[peaks])  #Print Magnitude of the peaks

    xf = np.linspace(0.0, 1.0/(2.0*T), int(n/2))
    #xf = np.linspace(0.0, T*rate, int(n/2))
    one_side = np.abs(fft[:n//2])
    #peak_one_side = np.abs(peaks[:n//2])
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
    file_path = "dn3.wav"
    samples, sampling_rate = librosa.load(file_path, sr = None, mono = True, offset = 0.0, duration = None)
    sound_fft(samples, sampling_rate)

if __name__ == '__main__':
    main()
