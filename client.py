from ast import Return
import socket
from typing_extensions import Self
from urllib import response
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "localhost"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

class robot:
    def send(self, msg):
        # accept dictionary of status
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        response_mgs = client.recv(2048).decode(FORMAT)
        print(response_mgs)
        return response_mgs
    
    def wait(order, pos):
        while order == '2':
            time.sleep(5)
            print('Resend position ' + pos)
            message = pos.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            client.send(send_length)
            client.send(message)
            order = client.recv(2048).decode(FORMAT)
