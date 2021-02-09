import os 
import sys
import math
import array
import librosa
from librosa import display
from matplotlib import pyplot as plt 
import scipy
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np
from peakdetect import peakdetect
from numpy import NaN, Inf, arange, isscalar, asarray, array


def sound_wave():
    file_path = "HP1.wav"
    samples, sampling_rate = librosa.load(file_path, sr = None, mono = True, offset = 0.0, duration = None)

    len(samples), sampling_rate
    l = len(samples)
    r = sampling_rate

    print("Number of samples is: %d" %l)     # Number of samples
    print("Number of samples per second is: %d " %r)    # We were capturing X amplitudes every second

    duration = len(samples)/sampling_rate   # How long was the audio
    print("Audio file was %.2f seconds long" %(duration))

    plt.figure()
    librosa.display.waveplot(y = samples, sr = sampling_rate)
    plt.xlabel("Time (seconds) -->")
    plt.ylabel("Amplitude")
    plt.show()

def sound_fft(sound, rate):
    n = len(sound)
    T = 1/rate
    yf = scipy.fft.fft(sound)

    yf = abs(yf)
    k = yf[1024]
    print(k)
    
    xf = np.linspace(0.0, 1.0/(2.0*T), int(n/2))
    #xf = np.linspace(0.0, T*rate, int(n/2))
    fig, ax = plt.subplots()
    #ax.plot(xf, 2.0/n * np.abs(yf[:n//2]))
    ax.plot(xf, np.abs(yf[:n//2]))

    plt.grid()
    plt.xlabel("Frequency")
    plt.ylabel("Magnitude")

    return plt.show()

def sample():
    samples = 100
    f = 3
    x = np.arange(samples)
    y1 = np.sin(2*np.pi*f * (x/samples))
    plt.figure()
    plt.stem(x,y1, 'r', )
    plt.plot(x,y1)
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.show()

    n = len(y1)
    T = 1/100
    yf = scipy.fft.fft(y1)
    xf = np.linspace(0.0, 1.0/(2.0*T), int(n/2))
    fig, ax = plt.subplots()
    ax.plot(xf, 2.0/n * np.abs(yf[:n//2]))
    plt.grid()
    plt.xlabel("Freq")
    plt.ylabel("Mag")
    plt.show()

"""
def plot_fft():
peaks = peakdetect(data, lookahead=20) 
# Lookahead is the distance to look ahead from a peak to determine if it is the actual peak. 
# Change lookahead as necessary 
higherPeaks = np.array(peaks[0])
lowerPeaks = np.array(peaks[1])
plt.plot(data)
plt.plot(higherPeaks[:,0], higherPeaks[:,1], 'ro')
plt.plot(lowerPeaks[:,0], lowerPeaks[:,1], 'ko')
"""
def main():

    file_path = "dn2.wav"
    samples, sampling_rate = librosa.load(file_path, sr = None, mono = True, offset = 0.0, duration = None)
    #sound_fft(samples, sampling_rate)

    #yf = scipy.fft.fft(samples)
    #kf = scipy.fft.fft(samples)
    yf = np.fft.fft(samples)
    kf = np.fft.fft(samples)
    #print(yf)
    yf= abs(yf)
    kf = np.abs(kf)
    peaky = np.max(kf)
    print(peaky)
    locY = np.argmax(kf)
    #print(locY)
    #frqY = frq

    peaks,_ = find_peaks(yf, height=10)
    #print(peaks)            #freq
    print(peaks[0])
    print(yf[peaks[0]])
    lenght = len(peaks)
    print("length of peaks is", lenght)
    #print(yf[peaks])        #mag
    #print(yf)
 
    f = []
    h = []
    g = []
    q = []
    j = 0 
    l = 1

    for k in range(8000):
        f[k] = f.append(0)
        #h[k] = h.append(0)
        g[k] = g.append(0)
    for k in range (0, lenght):
        q[k] = q.append(0)
        h[k] = h.append(0)
    
    for i in range (0, len(peaks)):
        q[i] = yf[peaks[i]]
        h[i] = q[i]

    q.sort(reverse = True)
    print(q[0])
    a = q[0]
    print("A is:", a)
    #print(h)

    index1 = np.where(yf == q[0])
    index2 = np.where(yf == q[2])
    index3 = np.where(yf == q[4])
    index4 = np.where(yf == q[6])
    print("Your 1st top freq is:", index1)
    print("Your 2nd top freq is:", index2)
    print("Your 3rd top freq is:", index3)
    print("Your 4th top freq is", index4)
   
    g[k] = yf[0]

    for i in range(0,8000):
        f[i] = (yf[i])
        #h[j] = f[i]
        #j = j + 1
        if (f[i] > g[k]):
            #print("l big than i")
            g[k] = f[i]
            #print(i)
            n = i
        #else:
            #print("nothing")
            
        #l = l + 1
        #print(f[i])
    #print(yf[393])
    print(n)
    #k = sorted(f, reverse = True)
    #h = sorted(h, reverse = True)

    #print(k)
    #print(k)
    #print(h)
    #print(k)
    #print(p)
    #print(o)
    #print(peaks)
    plt.plot(yf)
    plt.plot(peaks, yf[peaks], 'x')
    plt.show()

if __name__ == '__main__':
    main()
