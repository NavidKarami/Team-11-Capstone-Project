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

def voice():
    print("\nWhen you are ready to record, press 'r' and hit 'enter' on your keyboard.")
    print("There is a slight delay after your keyboard input. You will be prompted when to speak.")
    print("The phrase you need to say is: This is ________")
    u_input = str("k")
    while (u_input != "r"):
        print("\nPress 'r'  and hit 'enter' when ready.")
        u_input = input()
    
    #print("please speak a word into the microphone after the displayed delay")
    record_to_file('audio.wav')
    print("done")
    ##########would go to FFT analysis here
    main()











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
            print("\nThe pin does not match. Try again.")
        else:
            break
    # Store the pincode in the system
    user.pin.append(pinnum)



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
        exit()
        #voice()

    # If the input doesn't match the user's pin, then we get error message.
    # User gets 3 attempts before being locked out.
    print("Incorrect pin. Try again.")
    user.count = user.count + 1 
    if (user.count == 3):
        print("Too many attempts. Locking you out for 10 sec.")
        time.sleep(10)  # time that user gets locked out (in sec)
        user.count = 0
        main()  # do we want to go to main or just have them restart pin attempts?##########
    current_user_pin(index)  # call the pin function again



def userinfo():
    # Prints out users and passwords, using for testing purposes only
    z = 0
    k = 0
    x = len(user.name)
    y = len(user.pin)
    print("\nRegistered users: ")
    while (z < x):
        print(user.name[z])
        z += 1
    print("\nPins:")
    while (k < y):
        print(user.pin[k])
        k += 1


def main():
    print("\nWELCOME!")
    # This is the main menu for our program.
    # Any number that isn't a valid option will get an error message.
    # Program runs until the user terminates it.
    while True:
        print("\n[1]: New user\n[2]: Current user\n[3]: TESTING PHASE (View User Info)\n[4]: Exit")
        select = input("Please select from the options above: ")
        if (select == '1'):
            newuser()
        elif (select == '2'):
            currentuser()
        elif (select == '3'):
            userinfo()
        elif (select == '4'):
            exit()
        else:
            print("\nError. Invalid input. Try again.")


if __name__ == '__main__':
    main()

