from Client import robot
import time
from update_query import query_check


status = 'Standby'
position = ['start','E', 'D', 'G', 'A', 'H', 'B', 'C', 'D', 'F']
name = "Robot-Y"
battery = 100.0
status = '3'
current_pos = 'standby'

robot_a = robot(name ,current_pos, status, battery)
for mess in position:
    robot_a.position = mess
    msg = robot_a.name+ " is sending " + robot_a.position
    battery -= 1
    robot_a.battery = battery
    result = robot_a.send()
    print('Current position is '+ robot_a.position)
    print('battery is '+ str(robot_a.battery))
    query_check.update(robot_a.position,robot_a.status, 
                       robot_a.battery, robot_a.name)
    robot.wait(result,robot_a.position)
    time.sleep(5)

robot_a.send_disconnect()