from sys import path
path.append("/home/pi/TMotorCANControl/src/")
from TMotorCANControl.servo_serial import *
from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop

Type = 'AK80-9'
duty = 0.1

with TMotorManager_servo_serial(motor_type=Type,port = '/dev/ttyUSB1') as dev:
        loop = SoftRealtimeLoop(dt=0.005, report=True, fade=0.0)
        dev.set_zero_position()
        dev.update()
        
        dev.enter_duty_cycle_control()
        
        for t in loop:
            dev.set_duty_cycle_percent(duty)
            dev.update()
            print(f"\r {dev}", end='')

        