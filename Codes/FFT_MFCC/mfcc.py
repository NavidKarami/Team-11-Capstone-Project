import numpy
import scipy.io.wavfile
from scipy.fftpack import dct
import numpy as np
import xlwt
from xlwt import Workbook

def mfcc_compare(database, audio_mfcc):
    len_audio_mfcc = len(abs(audio_mfcc))

    m1_bottom_mfcc1 = sorted((abs(audio_mfcc[0])),reverse = True)                  
    m2_bottom_mfcc1 = sorted((abs(audio_mfcc[1])),reverse = True)
    m3_bottom_mfcc1 = sorted((abs(audio_mfcc[2])),reverse = True)
    m4_bottom_mfcc1 = sorted((abs(audio_mfcc[3])),reverse = True)
    m5_bottom_mfcc1 = sorted((abs(audio_mfcc[4])),reverse = True)
    m123_bottom = np.concatenate((m1_bottom_mfcc1,m2_bottom_mfcc1,m3_bottom_mfcc1,m4_bottom_mfcc1,m5_bottom_mfcc1))

    fdrift = 20
    match = []
    nomatch_index = []
    index_match = []
    i = 0
    for sample in database:                     #Perform a one-to-one comparison between the database and the loaded audio file (m12345_bottom)
        if ((m123_bottom[i]-fdrift)<=sample<=(m123_bottom[i]+fdrift)):
            index_match.append(i)
            match.append(1)                                 
        else:
            nomatch_index.append(i)             #It keeps track of the index which did not match
        i = i + 1

    print((len(match))/(len(database)))

    if len(match)>= len(m123_bottom)*0.70:      #as we increase 0.8, we increase the accuracy expectation. Right now we want 80% of the data match with database
        print('Welcome ')#, name)
        flag = 1
    else:
        print('Authentication Failed')
        flag = 0

    return flag

def mfcc_database(mfcc_data_1, mfcc_data_2, mfcc_data_3, mfcc_data_4, mfcc_data_5):
    # Get the len of each audio file mfcc array. We want to know how many values are in each
    len_mfcc_1 = len(abs(mfcc_data_1))
    len_mfcc_2 = len(abs(mfcc_data_2))
    len_mfcc_3 = len(abs(mfcc_data_3))
    len_mfcc_4 = len(abs(mfcc_data_4))
    len_mfcc_5 = len(abs(mfcc_data_5))

    #mfcc1 stands for audio #1, mfcc2 stands for audio #2....
    #each audio file can have up to 200+ coeff and each coeff has 12 values in it
    #we are looking at the five coeff - each having 12 values
    #bottom refers to values at the begining of the array test = [a,b,c....x,y,z] a,b and c are the at the bottom and x,y,z are at top 
    m1_bottom_mfcc1 = sorted((abs(mfcc_data_1[0])),reverse = True)                                      
    m2_bottom_mfcc1 = sorted((abs(mfcc_data_1[1])),reverse = True)
    m3_bottom_mfcc1 = sorted((abs(mfcc_data_1[2])),reverse = True)
    m4_bottom_mfcc1 = sorted((abs(mfcc_data_1[3])),reverse = True)
    m5_bottom_mfcc1 = sorted((abs(mfcc_data_1[4])),reverse = True)

    #Extracting Audio file #2 mfcc values
    m1_bottom_mfcc2 = sorted((abs(mfcc_data_2[0])),reverse = True)
    m2_bottom_mfcc2 = sorted((abs(mfcc_data_2[1])),reverse = True)
    m3_bottom_mfcc2 = sorted((abs(mfcc_data_2[2])),reverse = True)
    m4_bottom_mfcc2 = sorted((abs(mfcc_data_2[3])),reverse = True)
    m5_bottom_mfcc2 = sorted((abs(mfcc_data_2[4])),reverse = True)

    #Extracting Audio file #3 mfcc values
    m1_bottom_mfcc3 = sorted((abs(mfcc_data_3[0])),reverse = True)
    m2_bottom_mfcc3 = sorted((abs(mfcc_data_3[1])),reverse = True)
    m3_bottom_mfcc3 = sorted((abs(mfcc_data_3[2])),reverse = True)
    m4_bottom_mfcc3 = sorted((abs(mfcc_data_3[3])),reverse = True)
    m5_bottom_mfcc3 = sorted((abs(mfcc_data_3[4])),reverse = True)

    #Extracting Audio file #4 mfcc values
    m1_bottom_mfcc4 = sorted((abs(mfcc_data_4[0])),reverse = True)
    m2_bottom_mfcc4 = sorted((abs(mfcc_data_4[1])),reverse = True)
    m3_bottom_mfcc4 = sorted((abs(mfcc_data_4[2])),reverse = True)
    m4_bottom_mfcc4 = sorted((abs(mfcc_data_4[3])),reverse = True)
    m5_bottom_mfcc4 = sorted((abs(mfcc_data_4[4])),reverse = True)
 
    #Extracting Audio file #5 mfcc values
    m1_bottom_mfcc5 = sorted((abs(mfcc_data_5[0])),reverse = True)
    m2_bottom_mfcc5 = sorted((abs(mfcc_data_5[1])),reverse = True)
    m3_bottom_mfcc5 = sorted((abs(mfcc_data_5[2])),reverse = True)
    m4_bottom_mfcc5 = sorted((abs(mfcc_data_5[3])),reverse = True)
    m5_bottom_mfcc5 = sorted((abs(mfcc_data_5[4])),reverse = True)

    #Create 2-D arrays to work with the above data coming from audio files mfcc
    rows, cols = (12, 12)
    m1_bottom_total = [[0]*cols]*rows
    m2_bottom_total = [[0]*cols]*rows
    m3_bottom_total = [[0]*cols]*rows
    m4_bottom_total = [[0]*cols]*rows
    m5_bottom_total = [[0]*cols]*rows

    #Adding the coeff indexes and divide them by 5 to get the average - five audio files, we are looking at five coeff of each and each coeff having 12 values 
    for ind in range(len(m1_bottom_mfcc1)):
        #print(m1_bottom_mfcc1[ind], m1_bottom_mfcc2[ind], m1_bottom_mfcc3[ind], m1_bottom_mfcc4[ind], m1_bottom_mfcc5[ind])
        m1_total = m1_bottom_mfcc1[ind] + m1_bottom_mfcc2[ind] + m1_bottom_mfcc3[ind] + m1_bottom_mfcc4[ind] + m1_bottom_mfcc5[ind]
        m2_total = m2_bottom_mfcc1[ind] + m2_bottom_mfcc2[ind] + m2_bottom_mfcc3[ind] + m2_bottom_mfcc4[ind] + m2_bottom_mfcc5[ind]
        m3_total = m3_bottom_mfcc1[ind] + m3_bottom_mfcc2[ind] + m3_bottom_mfcc3[ind] + m3_bottom_mfcc4[ind] + m3_bottom_mfcc5[ind]
        m4_total = m4_bottom_mfcc1[ind] + m4_bottom_mfcc2[ind] + m4_bottom_mfcc3[ind] + m4_bottom_mfcc4[ind] + m4_bottom_mfcc5[ind]
        m5_total = m5_bottom_mfcc1[ind] + m5_bottom_mfcc2[ind] + m5_bottom_mfcc3[ind] + m5_bottom_mfcc4[ind] + m5_bottom_mfcc5[ind]

        m1_bottom_total[ind] = m1_total/5
        m2_bottom_total[ind] = m2_total/5
        m3_bottom_total[ind] = m3_total/5
        m4_bottom_total[ind] = m4_total/5
        m5_bottom_total[ind] = m5_total/5
        
    #concatenate the results into one array
    m12345_bottom = np.concatenate((m1_bottom_total,m2_bottom_total,m3_bottom_total, m4_bottom_total, m5_bottom_total)) 
    #Return value is the database - it contains coeff from five audio files and each having total of 12. So, there are 60 values in it
    np.savetxt('tamarrdata.txt', m12345_bottom, fmt= '%f')
    b = np.loadtxt('tamarrdata.txt', dtype=float)
    print(m12345_bottom)
    print(b)
    return m12345_bottom

def mfcc_process(filename):
    sample_rate, signal = scipy.io.wavfile.read('%s.wav' %filename)
    #signal = signal[0:int(3.0 * sample_rate)]  # Keep the first 3.5 seconds

    pre_emphasis = 0.97
    emphasized_signal = numpy.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])

    frame_size = 0.025
    frame_stride = 0.01
    frame_length, frame_step = frame_size * sample_rate, frame_stride * sample_rate  # Convert from seconds to samples
    signal_length = len(emphasized_signal)
    frame_length = int(round(frame_length))
    frame_step = int(round(frame_step))
    num_frames = int(numpy.ceil(float(numpy.abs(signal_length - frame_length)) / frame_step))  # Make sure that we have at least 1 frame

    pad_signal_length = num_frames * frame_step + frame_length
    z = numpy.zeros((pad_signal_length - signal_length))
    pad_signal = numpy.append(emphasized_signal, z) # Pad Signal to make sure that all frames have equal number of samples without truncating any samples from the original signal

    indices = numpy.tile(numpy.arange(0, frame_length), (num_frames, 1)) + numpy.tile(numpy.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T
    frames = pad_signal[indices.astype(numpy.int32, copy=False)]

    frames *= numpy.hamming(frame_length)
    # frames *= 0.54 - 0.46 * numpy.cos((2 * numpy.pi * n) / (frame_length - 1))  # Explicit Implementation **

    NFFT = 512
    mag_frames = numpy.absolute(numpy.fft.rfft(frames, NFFT))  # Magnitude of the FFT
    pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))  # Power Spectrum

    nfilt = 40

    low_freq_mel = 0
    high_freq_mel = (2595 * numpy.log10(1 + (sample_rate / 2) / 700))  # Convert Hz to Mel
    mel_points = numpy.linspace(low_freq_mel, high_freq_mel, nfilt + 2)  # Equally spaced in Mel scale
    hz_points = (700 * (10**(mel_points / 2595) - 1))  # Convert Mel to Hz
    bin = numpy.floor((NFFT + 1) * hz_points / sample_rate)

    fbank = numpy.zeros((nfilt, int(numpy.floor(NFFT / 2 + 1))))
    for m in range(1, nfilt + 1):
        f_m_minus = int(bin[m - 1])   # left
        f_m = int(bin[m])             # center
        f_m_plus = int(bin[m + 1])    # right

        for k in range(f_m_minus, f_m):
            fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
        for k in range(f_m, f_m_plus):
            fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])
    filter_banks = numpy.dot(pow_frames, fbank.T)
    filter_banks = numpy.where(filter_banks == 0, numpy.finfo(float).eps, filter_banks)  # Numerical Stability
    filter_banks = 20 * numpy.log10(filter_banks)  # dB

    num_ceps = 12
    mfcc = dct(filter_banks, type=2, axis=1, norm='ortho')[:, 1 : (num_ceps + 1)] # Keep 2-13

    cep_lifter =22
    (nframes, ncoeff) = mfcc.shape
    n = numpy.arange(ncoeff)
    lift = 1 + (cep_lifter / 2) * numpy.sin(numpy.pi * n / cep_lifter)
    mfcc *= lift  #*

    filter_banks -= (numpy.mean(filter_banks, axis=0) + 1e-8)
    mfcc -= (numpy.mean(mfcc, axis=0) + 1e-8)

    return abs(mfcc), len(abs(mfcc))

def main():
    print("Database creation/MFCC comparison")
    # Create arrays to store each audio file info to them and pass them into mfcc_databse() function to create the database
    mfcc_coef_audio1 = []
    mfcc_coef_audio2 = []
    mfcc_coef_audio3 = []
    mfcc_coef_audio4 = []
    mfcc_coef_audio5 = []
 
    # Get each audio file mfcc coefficient and use it in mfcc_databse to create the database
    #mfcc_coef_audio1, len_mfcc_audio1 = mfcc_process('tamarr_tamarr_1')         
    #mfcc_coef_audio2, len_mfcc_audio2 = mfcc_process('tamarr_tamarr_2')
    #mfcc_coef_audio3, len_mfcc_audio3 = mfcc_process('tamarr_tamarr_3')
    #mfcc_coef_audio4, len_mfcc_audio4 = mfcc_process('tamarr_tamarr_4')
    #mfcc_coef_audio5, len_mfcc_audio5 = mfcc_process('tamarr_tamarr_5')


    # get the audio file mfcc values to be used in mfcc_compare()
    audio_mfcc,_ = mfcc_process('danny_tamarr_5')
    # data_bottom to be used in mfcc_compare - databottom is the database
    #data_bottom = mfcc_database(mfcc_coef_audio1, mfcc_coef_audio2, mfcc_coef_audio3, mfcc_coef_audio4, mfcc_coef_audio5)
    #print(data_bottom)
    #Pass the data_bottom which is our database and audio file to the mfcc_compare
    data_bottom = np.loadtxt('tamarrdata.txt', dtype=float) #s comes from the name and the data will be stored in a textfile
    print(data_bottom)
    mfcc_compare(data_bottom, audio_mfcc)

if __name__ == '__main__':
    main()
