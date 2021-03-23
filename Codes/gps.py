#GPS module code
#this code reads data from the usb port (your gps in this case)

import serial
try:
   gps = serial.Serial('COM3', 9600) #COM depends on your specific device
except:
   print('Failed to connect') #prints error if no device is connected
   exit()

while 1:
   line = gps.readline() #reads line from gps but this data is in bytes
   #print(line)
   #print(type(line))
   x = line.decode('UTF-8') #converts bytes to str data type
   #print(type(x))
   print(x)
   data = x.split(",") #split the string when a comma occurs
   if (data[0]=="$GNGLL"): #this is where the gps coordinates are located so we search for it
      #print(data)
      print(data[1], data[3]) #breakdown that specific line further
      lat = int(float(data[1])) #we get numbers but they are slightly skewed
      lon = int(float(data[3])) #NEED TO FIX THIS################
   #ALMOST DONE###############################################
      print("Your current GPS coordinates are:")
      print("Latitude: ", lat, "\nLongitude: -", lon)
      exit()      

fabkit.close()
