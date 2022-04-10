from email import message
import re
from Client import robot
import time
DISCONNECT_MESSAGE = "!DISCONNECT"
status = 'Standby'
position = ['A', 'B', 'C']
name = "Robot_X"
battery = 100.0
status = '3'
robot_a = robot()
for mess in position:
    msg = name+ " is sending " + mess
    result = robot_a.send(msg)
    print('Current position is '+ mess)
    robot.wait(result,mess)
    time.sleep(10)

robot_a.send(DISCONNECT_MESSAGE)