# Save as client.py  
# Message Sender 
import os 
from socket import * 
#host = "127.0.0.1" # set to IP address of target computer 
host = "192.168.31.54" # set to IP address of target computer 
port = 13000
addr = (host, port) 
UDPSock = socket(AF_INET, SOCK_DGRAM) 
while True: 
    data =input("Enter message to send or type 'exit': ")
    data= bytes(data,'utf-8')

   # b = data.encode('utf-8')
    print(type(data))
    UDPSock.sendto(data, addr) 
    
    if data == "exit": 
        break 
UDPSock.close() 
os._exit(0) 