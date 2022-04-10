from Client import robot
import time
DISCONNECT_MESSAGE = "!DISCONNECT"
status = 'Standby'
position = ['A', 'B', 'C']
name = "Robot_B"
robot_a = robot()
for mess in position:
    msg = name+ " is sending " + mess
    result = robot_a.send(msg)
    time.sleep(5)
robot_a.send(DISCONNECT_MESSAGE)