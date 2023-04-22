# Efficieny code: Cleaned and Rewritten

from sys import path
path.append("~/TMotorCANControl/src/")

from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
from NeuroLocoMiddleware.AdcManager import ADC_Manager
from TMotorCANControl.servo_can import TMotorManager_servo_can
from TMotorCANControl.servo_serial import *

import time
import csv
import numpy as np


torque_rating = 100  # 100 Nm = 5 V
def volt_to_torque(volt, bias=0):
    return (volt-2.5-bias)/2.5*torque_rating



d2 = TMotorManager_servo_serial(motor_type='AK10-9', port = '/dev/ttyUSB0', baud=961200)  # Driven, AK10-9
d1 = TMotorManager_servo_serial(motor_type='AK80-9', port = '/dev/ttyUSB1', baud=961200) # Driving AK80-9
fd = open("Measuring_efficiency_{}_A_antagonist{}.csv".format(time.time()),'w')
writer = csv.writer(fd)

SPEED_LIST = [1,4,8,12,16]
CURRENT_LIST = [1,4,8,12,16]

base_speed = 1
base_current = 0.1

loop = SoftRealtimeLoop(dt=0.005, report=True, fade=0.0)
def run(
        max_current: float = 0.0,
        max_velocity: float = 0.0,
        ramp_time: float =0.0,
        holding_time: float=0.0,
        frequency: int=0
):
    # Ramp up to set velocity;
    end_time = loop.time() + ramp_time
    d1.set_output_velocity_radians_per_second(max_velocity)
    d1.update()
    while(loop.time() < end_time):
        pass
    # Ramp to set current
    end_time = loop.time() + ramp_time
    d2.current_qaxis = max_current
    d2.update()
    while(loop.time() < end_time):
        pass
    
    # Start recording values:
    end_time = loop.time() + holding_time
    while(loop.time() > end_time):
        
    
        
    pass

d1.enter_velocity_control()
d2.enter_current_control()
d1.update()
d2.update()

speed_pos = 0
current_pos = 0

for t in loop:
    print(t)
    set_speed = SPEED_LIST[speed_pos]
    set_current = CURRENT_LIST[current_pos]
    run(current, speed, 0.5, 1, 0)
    current_pos += 1
    if(current_pos == len(CURRENT_LIST):
       speed_pos += 1
    if(speed_pos == len(SPEED_LIST):
       break
