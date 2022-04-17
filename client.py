from ast import Return
import socket
from typing_extensions import Self
from urllib import response
import time
import json

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
#SERVER = "localhost"
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

class robot:
    def __init__(self,name ,position, status, battery):
        self.name = name
        self.position = position
        self.status = status
        self.battery = battery

    def send(self):
        # accept dictionary of status
        bot_status = {
        'name' : self.name, 
        'position' : self.position,
        'status' : self.status,
        'battery' : self.battery
        }
        msg = json.dumps(bot_status)
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        response_mgs = client.recv(2048).decode(FORMAT)
        print(response_mgs)
        return response_mgs
    
    def send_disconnect(self):
        # disconnect to the server
        msg = "!DISCONNECT"
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        response_mgs = client.recv(2048).decode(FORMAT)
        print(response_mgs)
    
    def wait(order, name,  position, status, battery):
        i = 0
        if order == '2':
            while order != '1':
                i += 1
                # wait for 1 seconds 5 times
                time.sleep(1)
                bot_status = {
                'name' : name, 
                'position' : position,
                'status' : '2',
                'battery' : battery
                }
                msg = json.dumps(bot_status)
                
                print('Resend position ' )
                message = msg.encode(FORMAT)
                msg_length = len(message)
                send_length = str(msg_length).encode(FORMAT)
                send_length += b' ' * (HEADER - len(send_length))
                client.send(send_length)
                client.send(message)
                order = client.recv(2048).decode(FORMAT)
                print('Waited for {} second'.format(i))
                if i >= 5:
                    order = '1'
        
        elif order == '3':
            while order != '1':
                # wait for 2 seconds then resend position
                time.sleep(2)
                bot_status = {
                'name' : name, 
                'position' : position,
                'status' : '2',
                'battery' : battery
                }
                msg = json.dumps(bot_status)
                
                print('Resend position and wait for other robot to move out' )
                message = msg.encode(FORMAT)
                msg_length = len(message)
                send_length = str(msg_length).encode(FORMAT)
                send_length += b' ' * (HEADER - len(send_length))
                client.send(send_length)
                client.send(message)
                order = client.recv(2048).decode(FORMAT)
