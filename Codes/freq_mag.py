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

    peaks,_ = find_peaks(fft_one_side, distance=50, width=1, height=10, prominence=4, threshold=0.01) #Got rid of the unwanted X
    #this find the freq of the highest peak
    freq_h_peak = np.argmax(fft)

    #list of unsorted magnitudes
    mag_unsorted = fft_one_side[peaks]
    #sort the magnitudes in descending order and print it
    mag_sort_list = sorted(fft_one_side[peaks], reverse= True)
    #print("Mag sorted from highest to lowest:", mag_sort_list)

    #create an empty list of size mag_sort_list
    freq_index = [0]*len(mag_sort_list)
    #find the index/freq of magnitudes
    for k in range(0,len(mag_sort_list)):
        temp = mag_sort_list[k]
        freq_index[k] = np.where(fft_one_side == temp)[0][0]
    #print the freq 
    #print("Freq sorted from highest to lowest:", freq_index)
    xf = np.linspace(0.0, 1.0/(2.0*T), int(n/2))
    one_side = np.abs(fft[:n//2])
    
    plt.plot(one_side)
    plt.plot(peaks, fft[peaks], "x")
    plt.grid()
    plt.xlabel("Frequency")
    plt.ylabel("Magnitude")
    plt.show()

    return freq_index[:10]

def fft_compare(keyfreq,samplefreq):
    print('done')
    fdrift = 40                                                          
    match = []
    for sample in samplefreq:
        #print(sample)
        for key in keyfreq:
            #print(key)
            if (key-fdrift)<=sample<=(key+fdrift):
                match.append(1)
                break
    print(len(match))
    print(len(keyfreq))

    if len(match)>= len(keyfreq)*0.7:                                               #as we increase 0.7, we increase the accuracy expectation
        print('Hello Navid')
    else:
        print('Authentication Failed')

def main():
    #Load the audio file and perform FFT and find the top 10 freq - print them
    file_path1 = "tamarr2.wav"
    samples1, sampling_rate1 = librosa.load(file_path1, sr = None, mono = True, offset = 0.0, duration = None)
    keyfreq1 = sound_fft(samples1, sampling_rate1)
    print(keyfreq1)

    #Load the audio file and perform FFT and find the top 10 freq - print them
    file_path2 = "tamarr1.wav"
    samples2, sampling_rate2 = librosa.load(file_path2, sr = None, mono = True, offset = 0.0, duration = None)
    keyfreq2 = sound_fft(samples2, sampling_rate2)
    print(keyfreq2)

    #Compare the two audio files top 10 freqs
    fft_compare(keyfreq1,keyfreq2)

if __name__ == '__main__':
    main()
