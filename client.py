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
SERVER = "localhost"
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
    
    def wait(order, pos):
        i = 0
        while order == '2':
            i += 1
            time.sleep(5)
            print('Resend position ' + pos)
            message = pos.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            client.send(send_length)
            client.send(message)
            order = client.recv(2048).decode(FORMAT)
            print('Waited for {} loop'.format(i))
            if i >= 5:
                order = '1'
