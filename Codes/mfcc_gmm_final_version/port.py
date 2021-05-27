#It list your laptop/PC ports that are being used
#We use this code to find out what port our GPS module is connected to - "USB Serial Device"
import os
import sys
import serial
import serial.tools.list_ports

if __name__ == "__main__":
    ports = serial.tools.list_ports.comports()

    for port in ports:
        print(port.description)
