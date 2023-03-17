from sys import path
path.append("/home/pi/TMotorCANControl/src/")
from TMotorCANControl.servo_serial import *
from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
Type = 'AK10-9'
current = 2

with TMotorManager_servo_serial(motor_type=Type, port = '/dev/ttyUSB1') as dev:
        loop = SoftRealtimeLoop(dt=0.005, report=True, fade=0.0)
        dev.set_zero_position()
        dev.update()
        
        dev.enter_current_control()
        #dev.set_output_velocity_radians_per_second(1)
        #dev.set_motor_velocity_radians_per_second(2)
        #dev.set_output_torque_newton_meters(4)
       
        for t in loop:
            #dev.current_qaxis = current
            dev.set_motor_current_qaxis_amps(2)
            dev.update()
            print(f"\r {dev}", end='')

        