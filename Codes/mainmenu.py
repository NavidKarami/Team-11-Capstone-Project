# these were used for the main module (users/pins)
import os
import time
import sys
from array import *
import string
import numpy as np
import re

# used for the recording module
from sys import byteorder
from array import array
from struct import pack
import time as t
import pyaudio
import wave

THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

# used for FFT module (MFCC)
import numpy
import scipy.io.wavfile
from scipy.fftpack import dct
import numpy as np
import xlwt
from xlwt import Workbook

# used for the GPS module
import serial

def GPS():
    try:
        gps = serial.Serial('COM3', 9600) #COM depends on your specific device, second value is baudrate

    except:
        print('\nFailed to connect.') #prints error if no device is connected
        print('Try the following command in the prompt to see all available ports: \npython -m serial.tools.list_ports')
        main()

    while 1:
        line = gps.readline() #reads line from gps but this data is in bytes
        x = line.decode('UTF-8') #converts bytes to str data type
   
        data = x.split(",") #split the string when a comma occurs
        if (data[0]=="$GNGLL"): #this is where the gps coordinates are located so we search until we come across that line
            x = float(data[1]) #we get coordinates but they are in dddmm.mmmm format
            y = float(data[3])
            #print(x, y)
        #convert dddmm.mmmm to decimal degree format
            x1 = (x/100) - ((x%100)/100)
            x2 = (x%100)/60
            lat = x1 + x2
            y1 = (y/100) - ((y%100)/100)
            y2 = (y%100)/60
            lon = y1 + y2

        #check for correct +/- sign on coordinates
            if data[2] == 'N':
                lat = lat
            else:
                lat = lat*-1
            if data[4] == 'W':
                lon = lon*-1
            else:
                lon = lon
      
            print("\nYour current GPS coordinates are:")
            print("Latitude: ", lat, "\nLongitude: ", lon)
            exit()
    
    fabkit.close()


    
def mfcc_compare(database, audio_mfcc):
    len_audio_mfcc = len(abs(audio_mfcc))

    m1_bottom_mfcc1 = sorted((abs(audio_mfcc[0])),reverse = True)                  
    m2_bottom_mfcc1 = sorted((abs(audio_mfcc[1])),reverse = True)
    m3_bottom_mfcc1 = sorted((abs(audio_mfcc[2])),reverse = True)
    m123_bottom = np.concatenate((m1_bottom_mfcc1,m2_bottom_mfcc1,m3_bottom_mfcc1))
    #print(m123_bottom)
    
    fdrift = 18
    match = []
    nomatch_index = []
    index_match = []
    i = 0
    for sample in database:         #Perform a one-to-one comparison between the database and the loaded audio file (m12345_bottom)
        #print("Comparing " + str(sample) + " with " + str(int(m123_bottom[i])))
        if ((m123_bottom[i]-fdrift)<=sample<=(m123_bottom[i]+fdrift)):
            index_match.append(i)
            match.append(1)                                 
        else:
            nomatch_index.append(i)             #It keeps track of the index which did not match
        i = i + 1
    rate = (len(match)/len(database))*100
    print('\nVoice analysis complete.') 

    if len(match)>= len(database)*0.8:        #as we increase 0.8, we increase the accuracy expectation. Right now we want 80% of the data match with database
        print('Identity ')
        print('Your match rate is: ', rate)
        GPS()
    else:
        print('Authentication Failed')
        print('Your match rate is: ', rate)
        main()

def mfcc_database(mfcc_data_1, mfcc_data_2, mfcc_data_3):#########, mfcc_data_4, mfcc_data_5):
    # Get the len of each audio file mfcc array. We want to know how many values are in each
    len_mfcc_1 = len(abs(mfcc_data_1))
    len_mfcc_2 = len(abs(mfcc_data_2))
    len_mfcc_3 = len(abs(mfcc_data_3))
    #####len_mfcc_4 = len(abs(mfcc_data_4))
    #####len_mfcc_5 = len(abs(mfcc_data_5))

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
    ###m1_bottom_mfcc4 = sorted((abs(mfcc_data_4[0])),reverse = True)
    ###m2_bottom_mfcc4 = sorted((abs(mfcc_data_4[1])),reverse = True)
    #m3_bottom_mfcc4 = sorted((abs(mfcc_data_4[2])),reverse = True)
    #m4_bottom_mfcc4 = sorted((abs(mfcc_data_4[3])),reverse = True)
    #m5_bottom_mfcc4 = sorted((abs(mfcc_data_4[4])),reverse = True)
    #Extracting Audio file #5 mfcc values
    #####m1_bottom_mfcc5 = sorted((abs(mfcc_data_5[0])),reverse = True)
    #####m2_bottom_mfcc5 = sorted((abs(mfcc_data_5[1])),reverse = True)
    #m3_bottom_mfcc5 = sorted((abs(mfcc_data_5[2])),reverse = True)
    #m4_bottom_mfcc5 = sorted((abs(mfcc_data_5[3])),reverse = True)
    #m5_bottom_mfcc5 = sorted((abs(mfcc_data_5[4])),reverse = True)

    #Create 2-D arrays to work with the above data coming from audio files mfcc
    rows, cols = (12, 12)
    m1_bottom_total = [[0]*cols]*rows
    m2_bottom_total = [[0]*cols]*rows
    m3_bottom_total = [[0]*cols]*rows
    #####m4_bottom_total = [[0]*cols]*rows
    ####m5_bottom_total = [[0]*cols]*rows

    #Adding the coeff indexes and divide them by 5 to get the average - five audio files, we are looking at five coeff of each and each coeff having 12 values 
    for ind in range(len(m1_bottom_mfcc1)):
        m1_total = m1_bottom_mfcc1[ind] + m1_bottom_mfcc2[ind] + m1_bottom_mfcc3[ind] ######+ m1_bottom_mfcc4[ind] + m1_bottom_mfcc5[ind]
        m2_total = m2_bottom_mfcc1[ind] + m2_bottom_mfcc2[ind] + m2_bottom_mfcc3[ind] ######+ m2_bottom_mfcc4[ind] + m2_bottom_mfcc5[ind]
        m3_total = m3_bottom_mfcc1[ind] + m3_bottom_mfcc2[ind] + m3_bottom_mfcc3[ind] ######+ m3_bottom_mfcc4[ind] + m3_bottom_mfcc5[ind]
        ####m4_total = m4_bottom_mfcc1[ind] + m4_bottom_mfcc2[ind] + m4_bottom_mfcc3[ind] + m4_bottom_mfcc4[ind] + m4_bottom_mfcc5[ind]
        ####m5_total = m5_bottom_mfcc1[ind] + m5_bottom_mfcc2[ind] + m5_bottom_mfcc3[ind] + m5_bottom_mfcc4[ind] + m5_bottom_mfcc5[ind]
        m1_bottom_total[ind] = m1_total/3
        m2_bottom_total[ind] = m2_total/3
        m3_bottom_total[ind] = m3_total/3
        ####m4_bottom_total[ind] = m4_total/5
        ###3#m5_bottom_total[ind] = m5_total/5
    
    #concatenate the results into one array
    m123_bottom = np.concatenate((m1_bottom_total,m2_bottom_total,m3_bottom_total))#######, m4_bottom_total, m5_bottom_total)) 
    #Return value is the database - it contains coeff from five audio files and each having total of 12. So, there are 60 values in it
    return m123_bottom

def mfcc_process(filename):         # This is used to alter the audio recording made by the user to be used in MFCC analysis
    sample_rate, signal = scipy.io.wavfile.read('%s.wav' %filename)
    signal = signal[0:int(3.5 * sample_rate)]  # Keep the first 3.5 seconds

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
    mfcc *= lift

    filter_banks -= (numpy.mean(filter_banks, axis=0) + 1e-8)
    mfcc -= (numpy.mean(mfcc, axis=0) + 1e-8)

    return abs(mfcc), len(abs(mfcc))

def mfcc(index):
    # database values to be used in mfcc_compare 
    uzi = [256, 220, 136, 110, 90, 72, 67, 62, 55, 17, 9, 2, 177, 166, 140, 112, 90, 67, 60, 36, 32, 18, 7, 4, 126, 111, 102, 96, 80, 75, 67, 62, 43, 17, 12, 6]
    navid = [173,155,153,135,101,93,73,70,53,30,14,6,195,142,109,93,87,67,57,53,36,24,16,9,127,124,118,98,78,71,53,50,46,27,23,10]
    danny = [172,157,148,129,114,102,89,73,60,42,39,14,199,164,143,100,97,78,70,66,57,39,25,12,177,156,144,130,96,78,63,39,29,22,9,4]
    tamarr = [209,186,170,154,118,104,92,72,52,31,17,6,224,212,192,110,99,78,66,46,41,32,26,11,212,208,258,117,108,79,56,45,37,32,20,7]
    #sam = [170,142,120,105,80,57,44,37,30,20,9,3,158,95,81,60,56,53,38,32,21,53,39,37,32,26,19,15,14,5,3]

    if index == 0:
        database = uzi
    elif index == 1:
        database = navid
    elif index == 2:
        database = danny
    else:######### index == 3:
        database = tamarr
    ######else:
        ########database = sam
        
    print(database)
    if len(database) != 36:
        print("Value missing in database")
        print(len(database))
        exit()
    
    # get the audio file mfcc values to be used in mfcc_compare()
    audio_mfcc,_ = mfcc_process('audio')
    #Pass the test which is our database and audio file to the mfcc_compare
    mfcc_compare(database, audio_mfcc)

    

# from here down is all recording code
def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in range(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in range(int(seconds*RATE))])
    return r

def record():
    """
    Record a word or words from the microphone and 
    return the data as an array of signed shorts.
    Normalizes the audio, trims silence from the 
    start and end, and pads with 0.5 seconds of 
    blank sound to make sure VLC et al can play 
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h')
    #stopwatch(1)
    print("Say the phrase now.")
    while 1:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        if snd_started and num_silent > 30:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    #r = trim(r)
    #r = add_silence(r, 0.1)
    return sample_width, r

def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

def voice(index, rec):
    print("\nWhen you are ready to record, press 'r' and hit 'enter' on your keyboard.")
    print("There is a slight delay after your keyboard input. You will be prompted when to speak.")
    print("The phrase you need to say is: This is (yourname)")
    u_input = str("k")
    while (u_input != "r"):
        print("\nPress 'r'  and hit 'enter' when ready.")
        u_input = input()

    if rec == 1:
        record_to_file('audio1.wav')
        record_to_file('audio2.wav')
        record_to_file('audio3.wav')
        print("3 audio files made")
        print('should create database now (not sure how to save this though...)')
        # Create arrays to store each audio file info to them and pass them into mfcc_databse() function to create the database
        mfcc_coef_audio1 = []
        mfcc_coef_audio2 = []
        mfcc_coef_audio3 = []
        # Get each audio file mfcc coefficient and use it in mfcc_databse to create the database
        mfcc_coef_audio1, len_mfcc_audio1 = mfcc_process('audio1')         
        mfcc_coef_audio2, len_mfcc_audio2 = mfcc_process('audio2')
        mfcc_coef_audio3, len_mfcc_audio3 = mfcc_process('audio3')
        # call database module to create database based on these three recordings
############ make x be username of new user and somehow save this info
        x = mfcc_database(mfcc_coef_audio1, mfcc_coef_audio2, mfcc_coef_audio3)
        print(x)
        
    else:
        record_to_file('audio.wav')
        print("1 audio file made")
        mfcc(index)



# From here down, this is user/pin code.
class user:
    # This is the database for users and their pins. 
    # There is a one-to-one relationship between the name and pin.
    name = ["uzi", "navid", "danny", "tamarr"]
    pin = ['2218', '1000', '9999', '1234']
    count = 0  # count and trail are just counters
    trail = 0

def newuser():
    # New user module where user creates their username.
    print("\nWelcome New User!")
    while True:
        print("When entering your username, it can contain any character besides spaces.")
        name = input("Enter your username: ")
        check = bool(re.search(r"\s", name))

        #Check the input string for spaces or if the username is already taken.
        if (check == True):
            print("\nThe username contains a space! Please try again.")
            continue
        if name in user.name:
            print("\nThe username is being used. Please try again")
        else:
            break  
    # Stores the username in the system
    user.name.append(name)

    # Ask the user to create their four digit pin code.
    # If something other than 4 numbers are entered, error message will appear.
    print("\nCreate your pin. It may only be 4 digits.")
    while True: 
        pinnum = (input("Please enter your four-digit pincode: "))
        length = len(pinnum)
        if (pinnum.isdigit() == False) and (length != 4): #checks if both rules are violated
            print("\nInvalid pincode, the length is not four and needs to be digits only.")
        elif pinnum.isdigit() == False: # checks for numbers
            print("\nInvaild pincode, the pincode needs to be digits only.")
        elif length != 4:  # checks length
            print("\nInvaild pincode, the length of the pincode is not four.")
        else:
            break

    # Confirm the pin (by comparison)
    while True:
        pinnum2 = (input("\nPlease confirm your pin: "))
        if (pinnum != pinnum2):
            print("The pin does not match. Try again.")
        else:
            break
    print(name, "is now a registered user.")
    # Store the pincode in the system
    user.pin.append(pinnum)
    print('we should go to creating database now    call recording module')
    rec = 1
    index = 0
    voice(index, rec)

def currentuser():
    # This function is used to check if you are a current user in the code. 
    length_name = len(user.name) 
    temp_name = input("\nEnter your username: ")

    # Loop until you find the name in the database
    for k in range(0, length_name):
        if(temp_name == user.name[k]):
            user.trail = 0
            index = k   # Set the index so we know which element in the pin array we need to check
            current_user_pin(index) # Pass index to pin function

    # If the name isn't in the array, ask the user to re-enter name
    print("Invalid username. Try again.")
    user.trail = user.trail + 1 
    if (user.trail == 3):   # Keep track of the number of failed attempts
        user.trail = 0
        print("Too many attempts. Locking you out for 10 sec.")
        time.sleep(10)
        main()
    currentuser()

def current_user_pin(index):
    # This function is used to check the pin associated with the current user. 
    temp_pin = input("Enter your pin:")
    
    # If there's a match, username associated with that pin is displayed and we proceed to voice analysis
    if (str(temp_pin) == str(user.pin[index])):
        print("\nWelcome: ", user.name[index])
        user.count = 0
        print("Proceeding to voice analysis.")
        #exit()
        rec = 0
        voice(index, rec)

    # If the input doesn't match the user's pin, then we get error message.
    # User gets 3 attempts before being locked out.
    print("\nIncorrect pin. Try again.")
    user.count = user.count + 1 
    if (user.count == 3):
        print("Too many attempts. Locking you out for 10 sec.")
        time.sleep(10)  # time that user gets locked out (in sec)
        user.count = 0
        main()  # do we want to go to main or just have them restart pin attempts?##########
    current_user_pin(index)  # call the pin function again



def testing():
    print('\n\nYou can perform the following functional tests:')
    while True:
        print("\n[a]: Number of registered users\n[b]: Test GPS\n[c]: MFCC values maybe??\n[d]: Return to main menu")
        choice = input("Please select from the options above: ")
        if (choice == 'a'):
            z = 0
            x = len(user.name)
            print('\nRegistered users =', len(user.name))
        elif (choice == 'b'):
            print('\nTesting GPS module')
            GPS()
        elif (choice == 'c'):
            print('\nmaybe check the mfcc values?')
        elif (choice == 'd'):
            main()
        else:
            print('\nError, invalid input. Try again')



def main():
    print("\n\n\nWELCOME!")
    # This is the main menu for our program.
    # Any number that isn't a valid option will get an error message.
    # Program runs until the user terminates it.
    while True:
        print("\nMain Menu")
        print("[1]: New user\n[2]: Current user\n[3]: Functional tests\n[4]: Exit")
        select = input("Please select from the options above: ")
        if (select == '1'):
            newuser()
        elif (select == '2'):
            currentuser()
        elif (select == '3'):
            testing()
        elif (select == '4'):
            exit()
        else:
            print("\nError. Invalid input. Try again.")

if __name__ == '__main__':
    main()

