from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
try:
     from TMotorCANControl.mit_can import TMotorManager
except ModuleNotFoundError:
    from sys import path
    path.append("/home/pi/TMotorCANControl/src")
    from TMotorCANControl.mit_can import TMotorManager
import time

logvars = [
    "output_angle", 
    "output_velocity", 
    "output_acceleration",
    "current",
    "output_torque",
    "motor_angle", 
    "motor_velocity", 
    "motor_acceleration", 
    "motor_torque"
]

with TMotorManager(motor_type='AK80-9', motor_ID=3, CSV_file="log.csv",log_vars=logvars) as dev:
    dev.zero_position() # has a delay!
    time.sleep(1.5)
    dev.set_current_gains()
    
    loop = SoftRealtimeLoop(dt = 0.01, report=True, fade=0)
    for t in loop:
        dev.update()
        if t < 1.0:
            dev.τm = 0.0
        else:
            dev.τm = 0.1

    del loop