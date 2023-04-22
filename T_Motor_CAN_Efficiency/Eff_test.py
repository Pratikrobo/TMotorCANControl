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

bias = 0
torque_rating = 100  # 100 Nm = 5 V
def volt_to_torque(volt, bias=0):
    return (volt-2.5-bias)/2.5*torque_rating


SPEED_LIST = np.arange(1,20,1)
CURRENT_LIST = np.arange(1,15,1)

speed_alternate = []
# iterate over the original array
for i in range(len(SPEED_LIST)):
    # append the first and last elements in alternating order
    if i % 2 == 0:
        speed_alternate.append(SPEED_LIST[i // 2])
    else:
        speed_alternate.append(SPEED_LIST[-(i // 2 + 1)])
SPEED_LIST = np.array(speed_alternate)

current_alternate = []
# iterate over the original array
for i in range(len(CURRENT_LIST)):
    # append the first and last elements in alternating order
    if i % 2 == 0:
        current_alternate.append(CURRENT_LIST[i // 2])
    else:
        current_alternate.append(CURRENT_LIST[-(i // 2 + 1)])
CURRENT_LIST = np.array(current_alternate)


base_speed = 0
base_current = 0

def run(
        d1,
        d2,
        writer,       
        adc, 
        max_current: float = 0.0,
        max_velocity: float = 0.0,
        ramp_time: float =0.0,
        hold_time: float=0.0,
        frequency: int=0,
):
    dt = 1.0/frequency
    loop = SoftRealtimeLoop(dt=dt, report=True, fade=0.0)
    number_steps = int(ramp_time*frequency)
    dv = max_velocity/number_steps
    di = max_current/number_steps

    # Ramp up to set velocity;
    for i in range(0,number_steps):
        d1.set_output_velocity_radians_per_second(dv * (i+1))
        d2.current_qaxis = di * (i+1)
        d1.update()
        d2.update()

        time.sleep(dt)
    
    
    for t in loop:
        d1.set_output_velocity_radians_per_second(max_velocity)
        d1.update()
        d2.current_qaxis = max_current
        d2.update()
        #print("RUNNING")
        adc.update()
        writer.writerow([t, # "loop time (s)"
                        d1.get_output_velocity_radians_per_second(), #"velocity (Rad/S)"
                        volt_to_torque(adc.volts, bias=bias), #"Futek Torque (Nm)"
                        d1.get_voltage_bus_volts(), #"v_bus"
                        d1.get_current_bus_amps(), #"i_bus"
                        d1.get_voltage_qaxis_volts(), #"v_q"
                        d1.get_current_qaxis_amps(), #"i_q"
                        d1.get_voltage_daxis_volts(), #"v_d"
                        d1.get_current_daxis_amps(), #"i_d"
                        d2.get_output_velocity_radians_per_second(), #"velocity (Rad/S)"
                        d2.get_voltage_bus_volts(), #"v_bus"
                        d2.get_current_bus_amps(), #"i_bus"
                        d2.get_voltage_qaxis_volts(), #"v_q"
                        d2.get_current_qaxis_amps(), #"i_q"
                        d2.get_voltage_daxis_volts(), #"v_d"
                        d2.get_current_daxis_amps(), #"i_d"
                        max_velocity, #"des_speed"
                        max_current #"des_curr"
                        ])
        print("D1: ",d1.get_mosfet_temperature_celsius(), "D2: ",d2.get_mosfet_temperature_celsius())
                                    
        #print("Torue:",volt_to_torque(adc.volts, bias=bias), "Volts: ", adc.volts)
        if t > hold_time:
            break

    time.sleep(1)
        
    # Ramp down to set velocity;
    for i in range(0,number_steps):
        d1.set_output_velocity_radians_per_second(max_velocity -(dv * (i+1)))
        d2.current_qaxis = max_current - (di * (i+1))
        d1.update()
        d2.update()

        time.sleep(dt)

    time.sleep(1)


if __name__ == "__main__":

    frequency = 200
    ramp_time = 0.5
    hold_time = 1.0

    temp_thresh_upper = 45
    temp_thresh_lower = 37

    adc = ADC_Manager('ADC_backup_log.csv')
    with adc:
        adc.update()
        voltage_cal = []
        print("Calibrating Loadcell!!!")
        for i in range(500):
            #print("adc.volts: ",adc.volts)
            adc.update()
            voltage_cal.append(adc.volts)
        avg_volt = np.mean(np.array(voltage_cal))
        bias = avg_volt - 2.5
        print("Bias: {} V".format(bias))
        adc.update()    

    with open("Efficiency_{}.csv".format(time.time()),'w') as fd:
        writer = csv.writer(fd)
        writer.writerow(["loop time", # "loop time (s)"
                        "Output Velocity D1", #"velocity (Rad/S)"
                        "Futek Torque", #"Futek Torque (Nm)"
                        "V_BUS D1", #"v_bus"
                        "I_Bus D1", #"i_bus"
                        "V_q D1", #"v_q"
                        "I_q D1", #"i_q"
                        "V_d D1", #"v_q"
                        "I_d D1", #"i_d"
                        "Output Velocity D2", #"velocity (Rad/S)"
                        "V_BUS D2", #"v_bus"
                        "I_Bus D2", #"i_bus"
                        "V_q D2", #"v_q"
                        "I_q D2", #"i_q"
                        "V_d D2", #"v_q"
                        "I_d D2", #"i_d"
                        "max_velocity", #"des_speed"
                        "max_current" #"des_curr"
                        ])
        
        with TMotorManager_servo_serial(motor_type='AK80-9',port = '/dev/ttyUSB3', baud=961200) as d1: # Driving AK80-9
            with TMotorManager_servo_serial(motor_type='AK80-9',port = '/dev/ttyUSB2', baud=961200) as d2:  # Driven, AK80-9
                with adc:     
                
                    d1.enter_velocity_control()
                    d2.enter_current_control()
                    d1.update()
                    d2.update()
                    

                    for current in CURRENT_LIST:
                        for speed in SPEED_LIST:
                            print("Testing for:",speed,"rad/s", current,"amps")
                            run(d1, d2, writer, adc, current, speed, ramp_time, hold_time, frequency)
                            if(d1.get_mosfet_temperature_celsius() > temp_thresh_upper or d2.get_mosfet_temperature_celsius()>temp_thresh_upper):
                                while(True):
                                    print("Cooling Down, D1: ",d1.get_mosfet_temperature_celsius(), "D2: ",d2.get_mosfet_temperature_celsius())
                                    if(d1.get_mosfet_temperature_celsius() < temp_thresh_lower and d2.get_mosfet_temperature_celsius()<temp_thresh_lower):
                                        break
                                    d1.update()
                                    d2.update()
                                    
