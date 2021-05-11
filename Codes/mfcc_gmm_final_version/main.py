# used for the main module (users/pins)
import os
import time
import sys
from array import *
import string
import numpy as np

# used for FFT module (MFCC)
import numpy
import scipy.io.wavfile
from scipy.fftpack import dct
import numpy as np
import re    

#import all the function from recording module
from recording import *
#import all the functions from recording_newuser module
from recording_newuser import *  
#import all the functions from SpeakerIdentification module
from SpeakerIdentification import *
#import GPS module
from GPS import *

#####This is current user voice analysis module######
def voice_current(name, index, rec):
    print("\nWhen you are ready to record, press 'r' and hit 'enter' on your keyboard.")
    print("There is a slight delay after your keyboard input. You will be prompted when to speak.")
    print("The phrase you need to say is: This is (your name)")
    u_input = str("k")
    while (u_input != "r"):
        print("\nPress 'r' and hit 'enter' when ready to say your phrase")
        u_input = input()
        
    record_audio_test()
    mfcc_result = test_model(name)
    
    if mfcc_result == True:
        #print("Good")
        #exit(0)
        GPS()
        main()
    else:
        attempt = 2
        for a in range(attempt):
            print("We did not recognize you as", name,". Try again.")
            #print("Please say the phrase after the displayed delay.")
            record_audio_test()
            
            mfcc_result = test_model(name)
            if mfcc_result == True:
                exit(1)
                
        print("Too many attempts. Locking you out for 10 sec.")
        #time.sleep(10)  # time that user gets locked out (in sec)
        main()

# This class helps in user and pin module to keep track of number of users and attempts
class user:
    count = 0  # count and trail are just counters
    trail = 0
    username = []
    userpin = []

def newuser():
    # New user module where user creates their username.
    print("\nWelcome New User!")
    # load all the usernames
    user_file_path = "username.txt"
    user_path = open(user_file_path, 'r')
    i = 0
    for path in user_path:
        path = str(path.rstrip())
        user.username.insert(i, path)
        print(user.username[i])
        i = i + 1
    user_path.close()
    
    while True:
        print("When entering your username, it can contain any character besides spaces.")
        name = input("Enter your username: ")
        check = bool(re.search(r"\s", name))

        #Check the input string for spaces or if the username is already taken.
        if (check == True):
            print("\nThe username contains a space! Please try again.")
            continue
        if name in user.username:
            print("\nThe username is being used. Please try again")
        else:
            break  
    # Stores the username in the system and write it into the text file
    user_file_path = "username.txt"
    user_path = open(user_file_path, 'a')
    user_path.write("\n%s" %name)
    user.username.append(name)
    user_path.close()

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
    # Store the pincode in the system and write it into the text file
    pass_file_path = "password.txt"
    pass_path = open(pass_file_path, 'a')
    pass_path.write("\n%s" %pinnum)
    user.userpin.append(pinnum)
    pass_path.close()
    # we go to voice recording module now to create database for new user
    rec = 1
    index = 0
    # new user now needs to record 15 audio files for training purposes
    record_audio_train(name)
    # now that we recorded the 15 audio files, we train and create our model
    train_model(name)

def currentuser():
    user_file_path = "username.txt"
    user_path = open(user_file_path, 'r')
    i = 0
    for path in user_path:
        path = str(path.rstrip())
        user.username.insert(i, path)
        print(user.username[i])
        i = i + 1
    user_path.close()    
    # This function is used to check if you are a current user in the code. 
    #length_name = len(user.name)
    length_name = len(user.username) 
    temp_name = input("\nEnter your username: ")

    # Loop until you find the name in the database
    for k in range(0, length_name):
        if(temp_name == user.username[k]):
            user.trail = 0
            index = k   # Set the index so we know which element in the pin array we need to check
            current_user_pin(index, user.username) # Pass index to pin function

    # If the name isn't in the array, ask the user to re-enter name
    print("Invalid username. Try again.")
    user.trail = user.trail + 1 
    if (user.trail == 3):   # Keep track of the number of failed attempts
        user.trail = 0
        print("Too many attempts. Locking you out for 10 sec.")
        time.sleep(10)
        main()
    currentuser()

def current_user_pin(index, username):
    # This function is used to check the pin associated with the current user.
    pass_file_path = "password.txt"
    pass_path = open(pass_file_path, 'r')
    i = 0
    for path in pass_path:
        path = str(path.rstrip())
        user.userpin.insert(i, path)
        print(user.userpin[i])
        i = i + 1

    pass_path.close()
     
    temp_pin = input("Enter your pin:")
    
    # If there's a match, username associated with that pin is displayed and we proceed to voice analysis
    if (str(temp_pin) == str(user.userpin[index])):
        print("\nWelcome: ", username[index])
        user.count = 0
        print("Proceeding to voice analysis.")
        #exit()
        rec = 0
        voice_current(username[index], index, rec)

    # If the input doesn't match the user's pin, then we get error message.
    # User gets 3 attempts before being locked out.
    print("\nIncorrect pin. Try again.")
    user.count = user.count + 1 
    if (user.count == 3):
        print("Too many attempts. Locking you out for 10 sec.")
        time.sleep(10)  # time that user gets locked out (in sec)
        user.count = 0
        main()  # do we want to go to main or just have them restart pin attempts?##########
    current_user_pin(index, username)  # call the pin function again

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
    select = 0
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
            select = 0
            currentuser()
        elif (select == '3'):
            select = 0
            testing()
        elif (select == '4'):
            print("Program termindated.")
            exit()
        else:
            print("\nError. Invalid input. Try again.")

if __name__ == '__main__':
    main()