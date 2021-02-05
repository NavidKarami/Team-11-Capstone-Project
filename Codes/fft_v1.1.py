import os 
import math
import librosa
from librosa import display
from matplotlib import pyplot as plt 
import scipy
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np

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
    yf = np.abs(yf)
    peaks1,_ = find_peaks(yf, prominence=1)
    print(peaks1)
    xf = np.linspace(0.0, 1.0/(2.0*T), int(n/2))
    
    #finding the peaks

    fig, ax = plt.subplots()
    ax.plot(xf, 2.0/n * np.abs(yf[:n//2]))
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

def main():

    file_path = "navid3.wav"
    samples, sampling_rate = librosa.load(file_path, sr = None, mono = True, offset = 0.0, duration = None)
    sound_fft(samples, sampling_rate)

if __name__ == '__main__':
    main()
