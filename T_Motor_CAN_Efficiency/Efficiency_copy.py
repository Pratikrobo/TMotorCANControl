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

def write_to_csv(writer, data):
  writer.writerow(data)
  print("Hello from a function")

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
speed_test_array = np.linspace(-14,14,20)
current_test_array = np.linspace(-14,14,15)
#current_test_array = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
#speed_test_array = [1]

# pre_duty_test_array = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
# duty_test_array = []
# for d in pre_duty_test_array:
#     duty_test_array.append(d)
#     duty_test_array.append(0.0)

num_iters = len(speed_test_array)
step_duration = 1.0 # seconds

ERPM_to_RadPs = 2*np.pi/180/60 # (2/21)*9*(1/60)*(np.pi/180)

i = 0
prev_i = 0
iq_antagonist = 0
data = [1,1,1,1,1,1,1,1]
flag = True
with open("Measuring_efficiency_{}_A_antagonist{}.csv".format(iq_antagonist,time.time()),'w') as fd:
    writer = csv.writer(fd)
    writer.writerow(["timestamp (epoch)", "loop time (s)", "des velocity", "velocity (Rad/S)", "Futek Torque (Nm)","v_bus", "i_bus", "v_q", "i_q", "v_d", "i_d", "accel"])
    
    with TMotorManager_servo_serial(motor_type='AK10-9', port = '/dev/ttyUSB0', baud=961200) as dev:  # Driven, AK10-9
        with TMotorManager_servo_can(motor_type='AK80-9', motor_ID=41) as ser:    
        #with TMotorManager_servo_serial(motor_type='AK80-9', port = '/dev/ttyUSB0', baud=961200) as ser: # Driving AK80-9
            with ADC_Manager('ADC_backup_log.csv') as adc:                                  # FUTEK
                dev.enter_current_control()
                #dev.enter_duty_cycle_control()
                ser.enter_velocity_control()
                loop = SoftRealtimeLoop(dt=0.05, report=True, fade=0.0)
                for curr in current_test_array:
                    adc.update()
                    i = 0
                    t_next = step_duration + int(time.time())
                    print("testing with: {} rad\s".format(speed_test_array[i]))
                    time.sleep(0.1)
                    #for t in loop:
                    while True:
                        t = int(time.time())
                        adc.update()
                        
                        #if i == len(speed_test_array)/2 and flag:
                        #    start = time.time()
                            #while(ser.get_mosfet_temperature_celsius() >=35 or ser.get_mosfet_temperature_celsius()==0 or dev.get_mosfet_temperature_celsius() >=35 or dev.get_mosfet_temperature_celsius()==0):
                            #    print("Cooling DOWN: ",ser.get_mosfet_temperature_celsius()," , ",dev.get_mosfet_temperature_celsius())
                            #    dev.current_qaxis = 0
                            #    ser.set_output_velocity_radians_per_second(0)
                            #    ser.update()
                            #    dev.update()
                            #    time.sleep(2)
                            #end = time.time()
                            #t_next = t_next + end - start
                        #    flag = False


                        if t >= t_next:
                            #writer.writerow([time.time(), t, speed_test_array[i] , ser.get_output_velocity_radians_per_second(), volt_to_torque(adc.volts, bias=bias), ser.get_voltage_bus_volts(), ser.get_current_bus_amps(), ser.get_voltage_qaxis_volts(), ser.get_current_qaxis_amps()])
                        
                            #print("WRITTEN")
                            #print([time.time(), t,data[1]/data[0], data[2]/data[0], data[3]/data[0], data[4]/data[0], data[5]/data[0], data[6]/data[0], data[7]/data[0]])
                            t_next += step_duration
                            i += 1
                            
                            if i < num_iters:
                                print("testing with: {} rad\s".format(speed_test_array[i]))
                                
                            else:
                                break

                        #writer.writerow([0,0,0,0,0,0,0,0,0])            
                        ser.set_output_velocity_radians_per_second(speed_test_array[i])
                        #dev.set_duty_cycle_percent(curr)
                        #if(speed_test_array[i] > 0):
                        #    dev.current_qaxis = -curr
                        #else:
                        #    dev.current_qaxis = -curr
                        #print(volt_to_torque(adc.volts, bias=bias))
                        dev.current_qaxis = curr
                        #if(not ser.check_connection()):
                        #   print("SER DISCONNECTED")
                        #if (not dev.check_connection()):
                        #    print("DEV DISCONNECTED")
                        ser.update()
                        dev.update()
                        print(volt_to_torque(adc.volts, bias=bias))
                        # put this into an "update" function later and run ascynch
                        #data = read_packet(ser)
                        #if len(data):
                            #    p = parse_motor_parameters(data)
                            #    if p.initialized:
                            #        params = p
                            #ser.write(bytearray(comm_get_motor_parameters()))
                        #"des velocity", "velocity (Rad/S)", "Futek Torque (Nm)","v_bus", "i_bus", "v_q", "i_q"]
                        #data[0] = data[0] + 1 #Counter
                        #data[1] = data[1] + speed_test_array[i] #des velocity
                        #data[2] = data[2] + ser.get_output_velocity_radians_per_second() #velocity (Rad/S)
                        #data[3] = data[3] + volt_to_torque(adc.volts, bias=bias) #Futek Torque (Nm)
                        #data[4] = data[4] + ser.get_voltage_bus_volts() #v_bus
                        #data[5] = data[5] + ser.get_current_bus_amps() #i_bus
                        #data[6] = data[6] + ser.get_voltage_qaxis_volts() #v_q
                        #data[7] = data[7] + ser.get_current_qaxis_amps() #i_q

                        #if prev_i != i:
                        #    data = [time.time(), t, speed_test_array[i] , ser.get_output_velocity_radians_per_second(), volt_to_torque(adc.volts, bias=bias), ser.get_voltage_bus_volts(), ser.get_current_bus_amps(), ser.get_voltage_qaxis_volts(), ser.get_current_qaxis_amps()]
                        #    write_to_csv(writer, data)
                        #    print("WROTE")
                        #    prev_i = i

                        
                        #writer.writerow([time.time(), t, speed_test_array[i] , ser.get_output_velocity_radians_per_second(), volt_to_torque(adc.volts, bias=bias), ser.get_voltage_bus_volts(), ser.get_current_bus_amps(), ser.get_voltage_qaxis_volts(), ser.get_current_qaxis_amps(), ser.get_voltage_daxis_volts(), ser.ha(), ser.get_output_acceleration_radians_per_second_squared()])
                            #print(t)
                        #print(ser.get_mosfet_temperature_celsius()," , ",dev.get_mosfet_temperature_celsius()," , ",speed_test_array[i]," , ",curr," , ",ser.get_voltage_bus_volts())

                        

                        #writer.writerow([time.time(), t,data[1]/data[0], data[2]/data[0], data[3]/data[0], data[4]/data[0], data[5]/data[0], data[6]/data[0], data[7]/data[0]])
                            
                        #print(dev.get_output_velocity_radians_per_second())
                    #data = [0,0,0,0,0,0,0,0]
                    dev.current_qaxis = 0
                    dev.update()
                    print("Slowing down")
                    for spd in range(int(ser.get_output_velocity_radians_per_second()), 0,-1):
                        ser.set_output_velocity_radians_per_second(spd)
                        ser.update()
                        time.sleep(0.05)
                    print("Waiting")
                    time.sleep(2)
                    flag = True
                #    #spd = spd-1
                    #    #time.sleep(5)
                    #ser.set_output_velocity_radians_per_second(0)
                    #ser.update()
                    #while(ser.get_mosfet_temperature_celsius() >=35 or ser.get_mosfet_temperature_celsius()==0 or dev.get_mosfet_temperature_celsius() >=35 or dev.get_mosfet_temperature_celsius()==0):
                    #    print("Cooling DOWN: ",ser.get_mosfet_temperature_celsius()," , ",dev.get_mosfet_temperature_celsius())
                    #    ser.update()
                    #    time.sleep(2)













