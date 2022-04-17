from Client import robot
import time


status = 'Standby'
position = ['standby','E', 'D', 'G', 'H', 'A', 'B', 'C', 'D', 'F', 'standby']
name = "Robot-Y"
battery = 100.0
status = '3'
current_pos = 'standby'

robot_b = robot(name ,current_pos, status, battery)
for mess in position:
    robot_b.position = mess
    msg = robot_b.name+ " is sending " + robot_b.position
    robot_b.status = '1'
    battery -= 1
    robot_b.battery = battery
    result = robot_b.send()
    print('Current position is '+ robot_b.position)
    print('battery is '+ str(robot_b.battery))
    robot.wait(result, robot_b.name,  robot_b.position, robot_b.status, robot_b.battery)
    time.sleep(5)
print('out of loop')
robot_b.send_disconnect()