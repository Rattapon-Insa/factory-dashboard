from email import message
import socket 
import threading
import json

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def logic(msg):
    if 'A' in msg:
        return '2'
    else:
        return '1'

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            order = logic(msg)
            conn.send(order.encode(FORMAT))
            if msg == DISCONNECT_MESSAGE:
                connected = False
            
            if "{" in msg:
                message = json.loads(msg)
            else:
                message = msg

            """bot_status = {
            'name' : 'Robot-X', 
            'position' : 'standby',
            'status' : '3',
            'battery' : 100.0
            }"""
            print(f"[{addr}] {message}")

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()