from email import message
from Client import robot
import time
DISCONNECT_MESSAGE = "!DISCONNECT"
status = 'Standby'
position = ['start connection','A', 'B', 'C']
name = "Robot_X"
battery = 100.0
status = '3'
robot_a = robot()
for mess in position:
    msg = name+ " is sending " + mess
    result = robot_a.send(msg)
    robot_a.wait(result,msg)
    print('Now, I\'m at '+ mess)
    time.sleep(5)
robot_a.send(DISCONNECT_MESSAGE)