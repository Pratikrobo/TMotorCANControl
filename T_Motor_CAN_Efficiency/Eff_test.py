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

SPEED_LIST = [1,4,8,12,16]
CURRENT_LIST = [1,4,8,12,16]


def run(
        max_current: float = 0.0,
        max_velocity: float = 0.0,
        ramp_time: float =0.0,
        holding_time: float=0.0,
        frequency: int=0
):
    pass

# d2.enter_current_control()
# d1.enter_velocity_control()
# d2.update()
# d1.update()

loop = SoftRealtimeLoop(dt=0.005, report=True, fade=0.0)

for t in loop:
    print(t)
    for speed in SPEED_LIST:
        for current in CURRENT_LIST:
            run(current, speed, 0.5, 1, 0)


