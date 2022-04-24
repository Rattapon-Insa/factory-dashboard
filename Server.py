from email import message
import socket 
import threading
import json
from update_query import query_check

HEADER = 64
PORT = 5050
SERVER = '127.0.0.1'
#SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def logic(msg):
    name = msg['name']
    status_x, status_y = query_check.check_status()

    concern_point = {
        'G' : ['A'],
        'E' : ['C', 'D'],
        'C' : ['D', 'E'],
        'A' : 'case-2',
        'C' : 'case-2',
        'E' : 'case-2'
    }

    if status_x[1] == name:
        print('Robot-X sent the message')

        # Robot-X in the concern point
        current_pos_x = status_x[2]
        print('logic got X ' + current_pos_x)
        current_pos_y = status_y[2]
        print('logic got Y ' + current_pos_y)

        try:
            if current_pos_y in concern_point[current_pos_x]:
                # if both robot is in the concern position, then wait untill condition
                print('logic case 1')
                return '3'
            elif concern_point[current_pos_x] == 'case-2':
                print('logic case 2')
                return '2'
            else:
                print('logic case 3')
                return '1'
        except KeyError:
            print('logic case 3')
            return '1'

    else:
        print('Robot-Y sent the message')
        # Robot-Y in the concern point
        current_pos_x = status_x[2]
        current_pos_y = status_y[2]

        try:
            if concern_point[current_pos_y] == current_pos_x:
                # if both robot is in the concern position, then wait untill condition
                print(concern_point[current_pos_y])
                print('logic case 1')
                return '3'
            elif concern_point[current_pos_y] != current_pos_x:
                print(concern_point[current_pos_y])
                print('logic case 2')
                return '2'
            else:
                print('out of logic')
        except KeyError:
            print('logic case 3')
            return '1'

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if "{" in msg:
                message = json.loads(msg)
                name = message['name']
                pos = message['position']
                status = message['status']
                battery = message['battery']
                query_check.update(pos,status, 
                       battery, name)
                order = logic(message)
                conn.send(order.encode(FORMAT))
            else:
                message = msg
        
            if msg == DISCONNECT_MESSAGE:
                connected = False
            
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