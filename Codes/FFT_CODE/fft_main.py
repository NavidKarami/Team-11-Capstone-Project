import matplotlib.pyplot as plt
import numpy as np
import peakutils
from array import array
from scipy.fftpack import fft
from scipy.io import wavfile                                                   
np.set_printoptions(threshold=np.inf)

def plotfft(filename):
    fs, a = wavfile.read('%s.wav' %filename)                                    # load the data
    b=[(ele/2**8.)*2-1 for ele in a]                                            # this is 8-bit track, b is now normalized on [-1,1)

    c = fft(b)                                                                  # calculate fourier transform (complex numbers list)
    d = int(len(c)/2)                                                           # you only need half of the fft list (real signal symmetry)
    e = abs(c[:(d-1)])                                                          # amplitudes

    #calculating frequency domain x-labels
    k = np.arange(len(a))
    T = len(a)/fs                                                               # where fs is the sampling frequency
    frqLabel = k/T
    xlabel = frqLabel[:(d-1)]

    #calculating time domain x-labels
    Ts = 1/fs
    Tlabel = np.linspace(0,Ts*len(b),len(b))

    fig, ax = plt.subplots(1,2)
    ax[0].plot(xlabel,e,'r')
    ax[1].plot(Tlabel,a,'r')

    plt.savefig('%s.png' %filename)
    #plt.show()
    return e, xlabel                                                            # We are returning the amplitude and the x-axis

def find_peaks(xlabel,amp):                                                   

    peaks = peakutils.indexes(amp, thres=0.01, min_dist=220)       #find peaks above threshold returns index
    pk2amp = [0]
    ind = [0]
    for j, pk in enumerate(peaks):                                 #sort peaks from highest to lowest amplitude response 
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

    '''
    print(pk2amp)
    print(ind)                                                                  #Hence sort indeces to show frequencies at which highest to lowest response occurs 
    print(peaks[ind])
    print(xlabel[peaks[ind]])
    '''
    pkfreq = xlabel[peaks[ind]]
    keyfreq = pkfreq[:10]                                                       #Shows top 10 frequencies
    print(keyfreq)
    return keyfreq, pkfreq

def view_peaks(peaks1,peaks2):

    results = open('Resultdata.txt', 'w')                                       #Export data to result file
    results.write('Sample 1 data \n')
    results.write('%s \n' %peaks1)
    results.write('Sample 2 data \n')
    results.write('%s \n' %peaks2)

    results.close()

def fft_compare(keyfreq,samplefreq):
    print('done')
    fdrift = 50                                                               #82.5
    match = []
    for sample in samplefreq:
        for key in keyfreq:
            if (key-fdrift)<=sample<=(key+fdrift):
                match.append(1)
                break
    print(len(match))
    print(len(keyfreq))

    if len(match)>= len(keyfreq)*0.7:                                               #as we increase 0.7, we increase the accuracy expectation
        print('Hello Navid')
    else:
        print('Authentication failed')
       
amp1, xlabel1 = plotfft('demo1')                                                     #sample fft of demo 1. amp1 = e from plotfft()
keyfreq1, peaks1 = find_peaks(xlabel1, amp1)                                         #amp1 is = amp
"""
amp2, xlabel2 = plotfft('sample2')                                                   #Originally I was comparing two samples from the same user
keyfreq2, peaks2 = find_peaks(xlabel2, amp2)
"""
"""
np.save('sample', keyfreq2) #save it for database                                    #I am saving the sample to a file and wil use it as my database for comparison
b = np.load('sample.npy')
print(b)   
"""
keyfreq2 = np.load('navid_sample.npy')                                               #load the database for comparison against the original voice (keyfreq1)
fft_compare(keyfreq1,keyfreq2)                                                       #pass both keyfreq results to sesame() for comparison
