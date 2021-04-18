import matplotlib.pyplot as plt
import numpy as np
import peakutils
from array import array
from scipy.fftpack import fft
from scipy.io import wavfile
from scipy.signal import find_peaks                                                   
np.set_printoptions(threshold=np.inf)

def plotfft(filename):
    fs, a = wavfile.read('%s.wav' %filename)                                    # load the data. data is in the "a" variable 
    b=[(ele/2**8.)*2-1 for ele in a]                                            # this is 8-bit track, b is now normalized on [-1,1)

    c = fft(b)                                                                  # calculate fourier transform (complex numbers list)
    d = int(len(c)/2)                                                           # you only need half of the fft list (real signal symmetry)
    e = abs(c[:(d-1)])                                                          # get the abs value of half of the FFT spectrum

    #calculating frequency domain x-labels
    k = np.arange(len(a))
    T = len(a)/fs                                                               # where fs is the sampling frequency

    frqLabel = k/T
    #print(frqLabel)
    xlabel = frqLabel[:(d-1)]
    #print(xlabel)

    #calculating time domain x-labels
    Ts = 1/fs
    Tlabel = np.linspace(0,Ts*len(b),len(b))

    fig, ax = plt.subplots(1,2)
    ax[0].plot(xlabel,e,'b')
    ax[1].plot(Tlabel,a,'r')

    #plt.savefig('%s.png' %filename)
    #plt.show()
    return e, xlabel                                                            #We are returning the amplitude and the x-axis

def find_peak(xlabel,amp):                                                   

    peaks = peakutils.peak.indexes(amp, thres=0.01, min_dist=220)               #find peaks above threshold returns index

    pk2amp = [0]
    ind = [0]
    for j, pk in enumerate(peaks):                                              #sort peaks from highest to lowest amplitude response 
        #print(amp[pk])
        pkamp = amp[pk]                                        
        for i, point in enumerate(pk2amp):
            if pkamp > point:
                pk2amp.insert(i,pkamp)
                ind.insert(i,j)
                break
            elif i == (len(pk2amp)-1):
                pk2amp.append(pkamp)
                ind.insert(i,j)
    pk2amp = pk2amp[:-1]
    ind = ind[:-1]

    #print(peaks[ind])
    pkfreq = xlabel[peaks[ind]]
    #print(xlabel[635])
    keyfreq = pkfreq[0:4]                                                     #Shows the top freq - adjust the number as needed. With 4, you get the top four
    print(keyfreq)

    return keyfreq, pkfreq

def fft_compare(keyfreq,samplefreq):
    print('done')
    fdrift = 50                                                                #Tolerance +- of the peaks
    match = []
    new_match = []
    index_match = []
    nomatch_index = []

    test = [232.49, 362.18, 477.75, 120.55]                                     #This would be my database. If you don't want to use this database and want to compare two audio files. uncomment line 107 and change "for sample in test" to "for sample in samplefreq"                
  
    i = 0
    for sample in test:                                                   #Perform a one-to-one comparison between the database and the loaded audi file (keyfreq in this case)
        #print(sample)
        if ((keyfreq[i]-fdrift)<=sample<=(keyfreq[i]+fdrift)):
            #print(keyfreq[i])
            index_match.append(i)
            match.append(1)
        else:
            nomatch_index.append(i)
        i = i + 1

    print(len(match))
    print(len(keyfreq))

    if len(match)>= len(keyfreq)*0.7:                                               #as we increase 0.7, we increase the accuracy expectation
        print('Hello Navid')
    else:
        print('Authentication Failed')
       
amp1, xlabel1 = plotfft('tamarr_tamarr_3')                                          #sample fft of demo 1. amp1 = e from plotfft()
keyfreq1, peaks1 = find_peak(xlabel1, amp1)                                         #amp1 is = amp

amp2, xlabel2 = plotfft('tamarr_tamarr_2')                                          #Originally I was comparing two samples from the same user
keyfreq2, peaks2 = find_peak(xlabel2, amp2)

"""
#np.save('sample', keyfreq2) #save it for database                                   # I am saving the sample to a file and wil use it as my database for comparison
b = np.load('sample.npy')
print(b)   
"""
#keyfreq2 = np.load('navid_sample.npy')                                              #load the database for comparison against the original voice (keyfreq1)
fft_compare(keyfreq1,keyfreq2)                                                       #pass both keyfreq results to sesame() for comparison