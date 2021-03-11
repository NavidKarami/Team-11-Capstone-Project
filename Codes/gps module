import serial
try:
   fabkit = serial.Serial('COM3', 9600)
except:
   print('Failed to connect')
   exit()


y = 0
while 1:
   line = fabkit.readline()
   print(line)

fabkit.close()
