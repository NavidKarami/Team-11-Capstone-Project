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
from recording_currentuser import *
#import all the functions from recording_newuser module
from recording_newuser import *  
#import all the functions from SpeakerIdentification module
from voice_authentication import *
#import GPS module
from GPS import *

def voice_current(name, index):            # This is current user voice analysis module.
    print("\nWhen you are ready to record, press 'r' and hit 'enter' on your keyboard.")
    print("There is a slight delay after your keyboard input. You will be prompted when to speak.")
    print("The phrase you need to say is: This is (your name)")
    u_input = str("k")
    while (u_input != "r"):         # we wait for the user to press "r" and hit "enter"
        print("\nPress 'r' and hit 'enter' when ready to say your phrase")
        u_input = input()           # capture user input and check if it was "r" or no. If yes, go ahead if not loop until "r" pressed
        
    record_audio_test()             # we then call the audio recording code for the current user. It saves a sample.wav file in the current directory 
    mfcc_result = test_model(name)  # performs voice analysis and return true if passed and false if it did not
    # if the return value was true we get the GPS cordinates and return to the main menu
    if mfcc_result == True:
        GPS()
        main()
    #if the return value was false we allow user to try two more times before getting locked out for X# of seconds    
    else:
        attempt = 2
        for a in range(attempt):
            print("We did not recognize you as", name,". Try again.")
            record_audio_test()
            
            mfcc_result = test_model(name)
            if mfcc_result == True:
                GPS()
                main()
                
        print("Too many attempts. Locking you out for 10 sec.")
        time.sleep(10)              # time that user gets locked out (in sec)
        main()

# This class helps in user and pin module to keep track of number of users and attempts
class user: 
    trail = 0
    count = 0
    username = []
    userpin = []

def newuser():                              # New user module where user creates their username.
    print("\nWelcome New User!")
    user_file_path = "username.txt"         # load the username text file 
    user_path = open(user_file_path, 'r')
    i = 0
    for path in user_path:
        path = str(path.rstrip())
        user.username.insert(i, path)
        i = i + 1               # keep count of number of registered users 
    user_path.close()           # closes the file
    
    while True:                 # we are now asking the user to create their username
        print("When entering your username, it can contain any character besides spaces.")
        name = input("Enter your username: ")
        check = bool(re.search(r"\s", name))

        #Check the input string for spaces or if the username is already taken.
        if (check == True):     # if there's a space in the name, there is an error message
            print("\nThe username contains a space! Please try again.")
            continue
        if name in user.username:   # also error message if the username is already taken 
            print("\nThe username is being used. Please try again")
        else:
            break  
    # Stores the username in the system and writes/saves it in the text file
    user_file_path = "username.txt" 
    user_path = open(user_file_path, 'a')
    user_path.write("\n%s" %name)
    user.username.append(name)      # append the new username to the rest of the database
    user_path.close()

    # Ask the user to create their four digit pin code.
    # If something other than 4 numbers are entered, error message will appear.
    print("\nCreate your pin. It may only be 4 digits.")
    while True: 
        pinnum = (input("Please enter your four-digit pincode: "))
        length = len(pinnum)
        if (pinnum.isdigit() == False) and (length != 4):   #checks if both rules are violated
            print("\nInvalid pincode, the length is not four and needs to be digits only.")
        elif pinnum.isdigit() == False:                     # checks for numbers
            print("\nInvaild pincode, the pincode needs to be digits only.")
        elif length != 4:                                   # checks for length
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
    
    # Store the pincode in the system and writes/saves it into the text file
    pass_file_path = "password.txt"
    pass_path = open(pass_file_path, 'a')
    pass_path.write("\n%s" %pinnum)
    user.userpin.append(pinnum)     # append the pin to the rest of the database
    pass_path.close()
   
    # we go to voice recording module now to create database for new user
    # new user now needs to record 15 audio files for training purposes
    record_audio_train(name)
    # now that we recorded the 15 audio files, we train and create our model
    train_model(name)

def currentuser():                  # This function is for current users.
    user_file_path = "username.txt" # We are reading from the username text file which has all registered users. 
    user_path = open(user_file_path, 'r')
    i = 0   
    for path in user_path:
        path = str(path.rstrip())
        user.username.insert(i, path)
        i = i + 1
    user_path.close()       # closing the username text file
    length_name = len(user.username)  # Keeping track of the number of registered users
    temp_name = input("\nEnter your username: ") # asking for user input

    # Loop until you find the name in the database
    for k in range(0, length_name):
        if(temp_name == user.username[k]):
            user.trail = 0
            index = k       # Set the index so we know which element in the pin array we need to check
            current_user_pin(index, user.username) # Pass index and username to pin function

    # If the name isn't in the array, ask the user to try again
    print("Invalid username. Try again.")
    user.trail = user.trail + 1 
    if (user.trail == 3):   # Keep track of the number of failed attempts
        user.trail = 0      # if there are too many failed attempts, the program stops for a set time
        print("Too many attempts. Locking you out for 10 sec.")
        time.sleep(10)
        main()              # after the sleep time, we head back to the main menu
    currentuser()           # if the number of failed attempts isn't 3, we loop through this function again

def current_user_pin(index, username):  # Function for checking if pin matches current user logging in. 
    pass_file_path = "password.txt"     # We are opening and reading from the password text file. 
    pass_path = open(pass_file_path, 'r')
    i = 0
    for path in pass_path:              #read one word(str) at a time from the text file and removing the newline at the end
        path = str(path.rstrip())
        user.userpin.insert(i, path)    #saving the password into user class's userpin variable at the correct index (i)
        i = i + 1       # keeping track of the total number of saved passwords
    pass_path.close()   # we close the file and take the users input
    temp_pin = input("Enter your pin:")
    
    # If there's a match, username associated with that pin is displayed and we proceed to voice analysis
    if (str(temp_pin) == str(user.userpin[index])):
        print("\nWelcome: ", username[index])
        user.count = 0      # reset the count for the next person logging in
        print("Proceeding to voice analysis.")
        voice_current(username[index], index) # we call the current voice function to perform voice analysis
        
    print("\nIncorrect pin. Try again.")  # if the input doesn't match the user's pin, then we get error message
    user.count = user.count + 1 
    if (user.count == 3):               # user gets 3 attempts before being locked out
        print("Too many attempts. Locking you out for 10 sec.")
        time.sleep(10)  # time that user gets locked out (in sec)
        user.count = 0
        main()  # if we reach max attempts, we go back to main menu
    current_user_pin(index, username)  # call the pin function again until the user passes or fails 3 times

    
def main():                         # This is the main menu for our program.  
    select = 0
    print("\n\n\nWELCOME!")
    while True:
        print("\nMain Menu")        # Able to add new users, log in as a current user, and perform some functional tests. 
        print("[1]: New user\n[2]: Current user\n[3]: Exit")
        select = input("Please select from the options above: ")
        if (select == '1'):
            newuser()
        elif (select == '2'):       
            select = 0
            currentuser()
        elif (select == '3'):       # Program runs until the user terminates it.
            print("\nProgram terminated.")
            exit()                  
        else:                       # Any input that isn't a valid option will get an error message.
            print("\nError. Invalid input. Try again.")

if __name__ == '__main__':
    main()
