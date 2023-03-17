from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
# try:
#      from TMotorCANControl.TMotorManager import TMotorManager
# except ModuleNotFoundError:
from sys import path
path.append("/home/pi/TMotorCANControl/src/")
from TMotorCANControl.servo_can import TMotorManager_servo_can
import time


with TMotorManager_servo_can(motor_type='AK10-9', motor_ID=21) as dev:
    
    loop = SoftRealtimeLoop(dt=0.01, report=True, fade=0.0)
    dev.enter_current_control()
    for t in loop:
        dev.current_qaxis = -0.5
        dev.update()
        print(dev._motor_state)
        print(f"\r {dev}", end='')
