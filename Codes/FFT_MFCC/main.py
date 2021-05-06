# used for the main module (users/pins)
import os
import time
import sys
from array import *
import string
import numpy as np
import re

# used for FFT module (MFCC)
import numpy
import scipy.io.wavfile
from scipy.fftpack import dct
import numpy as np
import xlwt
from xlwt import Workbook

# used for the GPS module
import serial

from recording import *     # name the other files recording and mfcc or change these names to what you want
from mfcc import *

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


    
###################################################
    ################################ this only works for returning users not new users
def voice(name, index, rec):
    print("\nWhen you are ready to record, press 'r' and hit 'enter' on your keyboard.")
    print("There is a slight delay after your keyboard input. You will be prompted when to speak.")
    print("The phrase you need to say is: This is (your name)")
    u_input = str("k")
    while (u_input != "r"):
        print("\nPress 'r'  and hit 'enter' when ready.")
        u_input = input()

    print("Please say the phrase into the microphone after a short delay with normal tone and speed")
    record_to_file('demo1.wav')
    print("done - result written to demo1.wav")
    data_import = np.loadtxt('%sdata.txt' %name, dtype=float) #s comes from the name and the data will be stored in a textfile
    
    audio_mfcc,_ = mfcc_process('demo1') #demo1 gets stored into audio_mfcc after getting processed
    mfcc_result = mfcc_compare(data_import, audio_mfcc)
    if mfcc_result == True:
        GPS()
    else:
        attempt = 2
        for a in range(attempt):
            print("We did not recognize you as ",name,". Try again.")
            print("Please say the phrase after the short delay.")
            record_to_file('demo1.wav')
            audio_mfcc,_ = mfcc_process('demo1')
            mfcc_result = mfcc_compare(data_import, audio_mfcc)
            if mfcc_result == True:
                GPS()
                break
        print("Too many attempts. Locking you out for 10 sec.")
        time.sleep(10)  # time that user gets locked out (in sec)
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
            print("The pin does not match. Try again.")
        else:
            break
    print(name, "is now a registered user.")
    # Store the pincode in the system
    user.pin.append(pinnum)
    # we go to voice recording module now to create database for new user
    rec = 1
    index = 0
    ##############voice(name, index, rec)
    #need to call a different function. voice only has one recording... we need 5 recordings.
    # add this to the recording stuff?????

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
        voice(user.name[index], index, rec)

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
