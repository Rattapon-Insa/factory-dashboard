import serial

ser = serial.Serial(
    port='/dev/ttyUSB0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_TWO,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)

#print("connected to: " + ser.portstr)

while True:

    line = ser.readline()
    
    print(line)
    
ser.close()