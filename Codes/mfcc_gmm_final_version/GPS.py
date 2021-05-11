# used for the GPS module
import serial   

def GPS():
    g_flag = False
    try:
        gps = serial.Serial('COM5', 9600) #COM depends on your specific device, second value is baudrate

    except:
        print('\nFailed to connect.') #prints error if no device is connected
        print('Try the following command in the prompt to see all available ports: \npython -m serial.tools.list_ports')
        return False

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

            g_flag = True
            return print("\nYour current GPS coordinates are: \nLatitude: ", lat, "\nLongitude: ", lon)
    
    fabkit.close()
