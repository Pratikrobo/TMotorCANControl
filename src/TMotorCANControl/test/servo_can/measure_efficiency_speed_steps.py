from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
from NeuroLocoMiddleware.AdcManager import ADC_Manager
import time
import csv
import numpy as np
from sys import path
path.append("~/TMotorCANControl/src/")
from TMotorCANControl.servo_can import TMotorManager_servo_can
from TMotorCANControl.servo_serial import *
#from TMotorCANControl.test.servo_serial.Serial_manager_servo import *
import serial


torque_rating = 100  # 100 Nm = 5 V
def volt_to_torque(volt, bias=0):
    return (volt-2.5-bias)/2.5*torque_rating

bias = 0
with ADC_Manager('ADC_backup_log.csv') as adc:
    adc.update()
    voltage_cal = []
    print("Calibrating Loadcell!!!")
    for i in range(500):
        adc.update()
        voltage_cal.append(adc.volts)
    avg_volt = np.mean(np.array(voltage_cal))
    bias = avg_volt - 2.5
    print("Bias: {} V".format(bias))
    adc.update()


# v_min always 0
speed_test_array = [0.0, 5.0, 10.0, 12, 14, 16, 20, 22, 25]
speed_test_array = [10]

# pre_duty_test_array = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
# duty_test_array = []
# for d in pre_duty_test_array:
#     duty_test_array.append(d)
#     duty_test_array.append(0.0)

num_iters = len(speed_test_array)
step_duration = 3.0 # seconds

ERPM_to_RadPs = 2*np.pi/180/60 # (2/21)*9*(1/60)*(np.pi/180)

iq_antagonist = 0
 
with open("Measuring_efficiency_{}_A_antagonist{}.csv".format(iq_antagonist,time.time()),'w') as fd:
    writer = csv.writer(fd)
    writer.writerow(["timestamp (epoch)", "loop time (s)", "des velocity", "velocity (Rad/S)", "ADC Voltage (V)", "Futek Torque (Nm)", "Antagonist Q-Current (A)", "i_bus", "v_bus", "v_q", "i_q", "duty", "mosfet_temp","i_d","v_d","error"])
    
    with TMotorManager_servo_can(motor_type='AK10-9', motor_ID=31, CSV_file="log.csv") as dev:  # Driven
        with TMotorManager_servo_serial(port = '/dev/ttyUSB0', baud=961200, motor_params=Servo_Params_Serial['AK80-9']) as ser:                     # Driving
            with ADC_Manager('ADC_backup_log.csv') as adc:                                  # FUTEK
                adc.update()
                params = servo_serial_motor_state()
                #ser.write(bytearray(startup_sequence()))
                #ser.write(bytearray(set_motor_parameter_return_format_all()))
                
                loop = SoftRealtimeLoop(dt=0.05, report=True, fade=0.0)
                dev.enter_velocity_control()
                ser.enter_velocity_control()
                i = 0
                t_next = step_duration
                print("testing with: {} rad\s".format(speed_test_array[i]))
                time.sleep(0.1)
                for t in loop:
                    adc.update()

                    """if t >= t_next:
                        t_next += step_duration
                        i += 1
                        if i < num_iters:
                            print("testing with: {} rad\s".format(speed_test_array[i]))
                        else:
                            break

                    #dev.θd = speed_test_array[i]
                    #dev.update()
                    """
                    ser.set_output_velocity_radians_per_second(speed_test_array[i])
                    print(t)
                    ser.update()
                    # put this into an "update" function later and run ascynch
                    #data = read_packet(ser)
                    #if len(data):
                    #    p = parse_motor_parameters(data)
                    #    if p.initialized:
                    #        params = p
                    #ser.write(bytearray(comm_get_motor_parameters()))
          

                    #writer.writerow([time.time(), t, speed_test_array[i], dev.θd, adc.volts, volt_to_torque(adc.volts, bias=bias), iq_antagonist, params.input_current, params.input_voltage, params.Vq, params.iq_current, params.duty, params.mos_temperature, params.id_current, params.Vd, params.error])
                    # print("\r" + str(dev), end='')













