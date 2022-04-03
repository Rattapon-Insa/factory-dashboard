# Save as server.py  
# Message Receiver 
import os 
from socket import * 
host = "192.168.31.71" 
#host="127.0.0.1"
port = 13000
buf = 1024 
addr = (host, port) 
UDPSock = socket(AF_INET, SOCK_DGRAM) 
UDPSock.bind(addr) 
print ("Waiting to receive messages..." )
while True: 
   
    (data, addr) = UDPSock.recvfrom(buf)
    data = data.decode()
    print ("Received message: " + data )
    if data == "exit": 
        break 
UDPSock.close() 
os._exit(0) 