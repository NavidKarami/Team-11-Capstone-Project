'''
This is a mutiline comment 
User Input Pincode Module 
Name: Tamarr 
'''

# import the libarires 
import time 
import math
import numpy as np
import string

# number of elements in the array 
size = 10

class user:
    username = ['tommy', 'tim']
    pin = ['1234', '0000']


def NEWUSER():
    #New User Module 
    #Ask the user to type the name
    while True:
        print("Since you are new into our system")
        name = input("Enter your name\n")
        quit = True 
        for un in user.username:
            if(name == un):
                print("There is aleaday a username in the list")
                print("Please input your name again")
                quit = False
                break
        if(quit):
            break

    #Store the username in the system 
    user.username.append(name)
    print(user.username)

    
    #Ask the user for a four digit pin code 
    
    #if the four-digit wasn't entered properly, Ask the user agian 
    while True:
        #check the length and numbers only 
        pinnum = (input("Please enter your four-digit pincode\n"))
        #print(pinnum)
        length = len(pinnum)
        print(length)
        # Known: won't if you put in and 0000 within the pincode 
        if(length != 4):
            print("Invaild pincode, please try again!")
        else:            
           break
            

    print("This is the pincode\n")
    print(pinnum)
    
    while True:
        #Check if we have the same pincode 
        print("It's time to confirm your pincode")
        pinnum2 = (input("Please enter your four-digit pincode\n"))
        #print(pinnum2)
        length2 = len(pinnum2)
        #Confirm the four-digit pincode (Compare) 
        if(pinnum != pinnum2):
            print("The confirm pincode does not matched please try again")
        else:
            break 

    #Store the pincode in the system
    user.pin.append(pinnum)
    print(user.pin)
'''
* To check if an item is in a list, the "in" operator can be used 
* The in operator is alos used to determine whether or not a string is a substring of another string 
'''

def CURRENTUSER():

    print(user.username)
    #check if the currentname is in the user list
    #Ask the user to type the name
    while True:
        name = input("Enter your name\n")
        if name in user.username:
            print("Yes, you have" , name)
            break
        else:
            print("The username is not in list")
            print("Please try agian")
    
    test = 3
    while (test > 0):
        pinnum = (input("Please enter your four-digit pincode\n"))
        if pinnum in user.pin:
            print("Pincode Access Authorized")
            break
        else:
            print("Pincode is not recongized")
            print("Please try again")
            test -= 1
            print(test)
            if(test == 0):
                time.sleep(5)
                test = 3

def main():
    # User input
    while True: 
        # Open Menu 
        print('\nHello, Welcome to our Autheution Program!')
        print('Please enter the following key for Autheution\n')
        print('Enter [1]: Current User')
        print('Enter [2]: New User')
        print('Enter [3]: Exit\n')

        num = input('Enter your choice: ') 
        print(num)
        # Conditions 
        if (num == '1'):
            print('You are a current user!')
            print('Welcome back!')
            CURRENTUSER()
        elif (num == '2'):
            print('You decided to be a new user')
            NEWUSER();
        elif (num == '3'):
            print('You decided to exit the program')
            #time.sleep(5)
            exit()
        else:
            print("Invaild input, please try again")


if __name__ == "__main__":
    main()
