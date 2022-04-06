import socket
from test_client import robot
import time
DISCONNECT_MESSAGE = "!DISCONNECT"

all_position = ['standby', 'A', 'B', 'H',
                'D', 'F', 'G', 'C', 'B', 'I', 'standby']

def main():
    robot.name = 'Robot-Y'
    robot.status = "3"
    robot.battery = 100
    for position in all_position:
        robot.status = "1"
        robot.pos = position
        robot.send('{a}, {b}, {c}, {d}'.format(a = robot.name, b = robot.pos,
        c = robot.status, d = robot.battery))
        signal = robot.check()
        print(signal)
        while signal == 'wait':
            print("change status to wait")
            robot.status = "2"
            time.sleep(1)
            signal = robot.check()
        time.sleep(10)
        robot.battery -= 1
    robot.send(DISCONNECT_MESSAGE)

if __name__ == '__main__':
    main()