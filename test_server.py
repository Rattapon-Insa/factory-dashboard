import socket 
import threading
from update_query import query_check

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def check_logic_X(query):
    if query[1][1] == "Robot-X":
        R_X = query[1]
        R_y = query[0]
    else:
        R_X = query[0]
        R_y = query[1]
    print(R_X)
    print(R_y)
    print(R_X[2]," is the current postion of ", R_X[1])
    if R_X[2] == "A":
        A = R_X
        B = R_y              
        pos_a = "A"
        pos_b = 'C'
        final_pos_b = 'I'
        query_check.stop_go(A, B, pos_a, pos_b, final_pos_b)
    elif R_X[2] == "C":
        A = R_X
        B = R_y
        pos_a = "C"
        pos_b = 'A'
        final_pos_b = 'I'
        query_check.stop_go(A, B, pos_a, pos_b, final_pos_b)
    elif R_X[2] == "G":
        A = R_X
        B = R_y
        pos_a = "G"
        pos_b = 'H'
        final_pos_b = 'C'
        query_check.stop_go(A, B, pos_a, pos_b, final_pos_b)
    elif R_X[2] == "H":
        A = R_X
        B = R_y
        pos_a = "H"
        pos_b = 'G'
        final_pos_b = 'C'
        query_check.stop_go(A, B, pos_a, pos_b, final_pos_b)
    else:
        print('No condition met')

def check_logic_Y(query):
    if query[1][1] == "Robot-Y":
        R_X = query[1]
        R_y = query[0]
    else:
        R_X = query[0]
        R_y = query[1]
    print(R_X)
    print(R_y)
    print(R_X[2]," is the current postion of ", R_X[1])
    if R_X[2] == "A":
        A = R_X
        B = R_y 
        pos_a = "A"
        pos_b = 'standby'
        final_pos_b = 'I'
        query_check.stop_go(A, B, pos_a, pos_b, final_pos_b)
    elif R_X[2] == "C":
        A = R_X
        B = R_y
        pos_a = "C"
        pos_b = 'standby'
        final_pos_b = 'I'
        query_check.stop_go(A, B, pos_a, pos_b, final_pos_b)
    elif R_X[2] == "G":
        A = R_X
        B = R_y
        pos_a = "G"
        pos_b = 'standby'
        final_pos_b = 'C'
        query_check.stop_go(A, B, pos_a, pos_b, final_pos_b)
    elif R_X[2] == "H":
        A = R_X
        B = R_y
        pos_a = "H"
        pos_b = 'standby'
        final_pos_b = 'C'
        query_check.stop_go(A, B, pos_a, pos_b, final_pos_b)
    else:
        print('No condition met')


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            #print(f"[{addr}]{msg}")
            list_msg = msg.split(", ")
            if len(list_msg) == 4:
                name = list_msg[0]
                pos = list_msg[1]
                status = list_msg[2]
                battery = list_msg[3]
                query_check.update(pos, status, battery, name)
                ## this is one function take in =>> nothing
                ## function will fetch the current query data
                ## then, it will change the status in database based on the current condition
                query = query_check.fetch()
                if name == "Robot-X":
                    query_check.check_logic_X(query)
                if name == 'Robot-Y':
                    query_check.check_logic_Y(query)

                #if 'Z' in msg:
                    #conn.send("2".encode(FORMAT))
            conn.send("Server said, keep send me the massage".encode(FORMAT))

    conn.close() 

def start():
    print("[STARTING] server is starting...")
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

start()