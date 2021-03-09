import os 
import sys
import math
import array
import librosa
from librosa import display
from matplotlib import pyplot as plt 
import scipy
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_prominences, find_peaks_cwt
import numpy as np
from numpy import NaN, Inf, arange, isscalar, asarray, array
from collections import OrderedDict
from scipy.signal import argrelextrema
from scipy.signal import argrelmax

def sound_fft(sound, rate):

    n = len(sound)  #How long is the audio file
    T = 1/rate      #Sampling interval in time

    fft = scipy.fft.fft(sound) #Do FFT
    fft = abs(fft) #Get rid of the imaginary part

    #Compute FFT and get rid of the right side
    fft_one_side = np.abs(fft[:n//2])

    peaks,_ = find_peaks(fft_one_side, distance=30, width=1, height=30, prominence=4) #Got rid of the unwanted X
    #this find the freq of the highest peak
    freq_h_peak = np.argmax(fft)

    #list of unsorted magnitudes
    mag_unsorted = fft_one_side[peaks]
    #sort the magnitudes in descending order and print it
    mag_sort_list = sorted(fft_one_side[peaks], reverse= True)
    print(mag_sort_list)

    #create an empty list of size mag_sort_list
    freq_index = [0]*len(mag_sort_list)
    #find the index/freq of magnitudes
    for k in range(0,len(mag_sort_list)):
        temp = mag_sort_list[k]
        freq_index[k] = np.where(fft_one_side == temp)[0][0]
    #print the freq 
    print(freq_index)

    xf = np.linspace(0.0, 1.0/(2.0*T), int(n/2))
    one_side = np.abs(fft[:n//2])
    
    plt.plot(one_side)
    plt.plot(peaks, fft[peaks], "x")
    plt.grid()
    plt.xlabel("Frequency")
    plt.ylabel("Magnitude")
    plt.show()

def main():
    file_path1 = "H1.wav"

    samples1, sampling_rate1 = librosa.load(file_path1, sr = None, mono = True, offset = 0.0, duration = None)
    sound_fft(samples1, sampling_rate1)

if __name__ == '__main__':
    main()