from matplotlib import pyplot as plt
import csv
import numpy as np
import pandas as pd

name = "Measuring_efficiency_0_A_antagonist1682011472.1118934.csv"


data = pd.read_csv(name)
print([k for k in data])

# timestamp (epoch)
# loop time (s)
# des velocity
# velocity (Rad/S)
# Futek Torque (Nm)
# v_bus
# i_bus
# v_q
# i_q
# v_d
# i_d
# accel
torque_adc_raw = -1*np.array(data['Futek Torque (Nm)'])
time_raw = np.array(data['loop time (s)'])
v_bus_raw = np.array(data['v_busM'])
i_bus_raw = np.array(data['i_busM'])
i_q_raw = np.array(data['i_qM'])
v_q_raw = np.array(data['v_qM'])
speed_raw = np.array(data['velocityM (Rad/S)'])
des_curr_raw = np.array(data['des current'])
i_d_raw = np.array(data['i_dM'])

data_avg = [0,0,0,0,0,0,0,0]

torque_adc = np.array([])
counter = np.array([])
v_bus = np.array([])
i_bus = np.array([])
i_q = np.array([])
v_q = np.array([])
speed = np.array([])
i_d = np.array([])
## Average out the values
i = 0
j = 0
#print( len(torque_adc_raw)-5)


while i< len(torque_adc_raw):
    desired_curr = des_curr_raw[i]
    data_avg[0] = data_avg[0]+1 # Counter
    data_avg[1] = data_avg[1]+torque_adc_raw[i] # Torque_adc
    data_avg[2] = data_avg[2]+v_bus_raw[i] # V_bus
    data_avg[3] = data_avg[3]+i_bus_raw[i] # I_Bus
    data_avg[4] = data_avg[4]+v_q_raw[i] # V_q
    data_avg[5] = data_avg[5]+i_q_raw[i] # I_q
    data_avg[6] = data_avg[6]+speed_raw[i] # Speed
    data_avg[7] = data_avg[7]+np.absolute(i_d_raw[i]) # I_d
    i = i+1
    print("i:",i)
    while(des_curr_raw[i] == desired_curr):
        
        data_avg[0] = data_avg[0]+1 # Counter
        data_avg[1] = data_avg[1]+torque_adc_raw[i] # Torque_adc
        data_avg[2] = data_avg[2]+v_bus_raw[i] # V_bus
        data_avg[3] = data_avg[3]+i_bus_raw[i] # I_Bus
        data_avg[4] = data_avg[4]+v_q_raw[i] # V_q
        data_avg[5] = data_avg[5]+i_q_raw[i] # I_q
        data_avg[6] = data_avg[6]+speed_raw[i] # Speed
        data_avg[7] = data_avg[7]+np.absolute(i_d_raw[i]) # I_d
        i = i+1
        if i == len(torque_adc_raw):
            break
        
    #print(torque_adc)
    #print(data_avg[1]/data_avg[0])
    #data_avg[0] = data_avg[0]+1 # Counter
    data_avg[1] = data_avg[1]/data_avg[0] # Torque_adc
    data_avg[2] = data_avg[2]/data_avg[0]# V_bus
    data_avg[3] = data_avg[3]/data_avg[0] # I_Bus
    data_avg[4] = data_avg[4]/data_avg[0] # V_q
    data_avg[5] = data_avg[5]/data_avg[0] # I_q
    data_avg[6] = data_avg[6]/data_avg[0] # Speed
    data_avg[7] = data_avg[7]/data_avg[0] # I_d
    if (data_avg[6] >= -1 and data_avg[1]>=0) or True:
        torque_adc = np.append(torque_adc,data_avg[1])
        v_bus = np.append(v_bus,data_avg[2])
        i_bus = np.append(i_bus,data_avg[3])
        i_d = np.append(i_d,data_avg[4])
        v_q = np.append(v_q,data_avg[5])
        speed = np.append(speed,data_avg[6])
        i_q = np.append(i_q,data_avg[7])
        counter = np.append(counter,j)
        j = j+1
        data_avg = [0,0,0,0,0,0,0,0]
        print("data_avg[2]:",data_avg[2])

print()
#print(i_d)


#print(i_d)

#print("speed:",speed)
#print("vbus:",v_bus)
#print("ibus:",i_bus)
#print("torque:",torque_adc)

power_out = torque_adc*speed
power_in = v_bus*i_bus
eff = np.zeros_like(power_out)
for i in range(power_out.shape[0]):
    tmp = 100*power_out[i]/power_in[i]
    
    print("P In:",power_in[i])
    print("P out:",power_out[i])
    #if tmp<=-100:
    #    tmp = -100
    eff[i] = tmp if ((not np.isnan(tmp) and not np.isinf(tmp))) else -100
    print(" eff[i]:", eff[i])
#print(eff)
#print(np.mean(eff))
#print(np.max(eff))

# print(data)
#print("Average Torque: {}Nm".format(torque_adc.mean()))

# plt.plot(time_array, torque_array)
# plt.savefig("torque_plot_{}_A.png".format(iq_des))

# plt.plot(time,torque_adc,label="τ_adc (max: " + str(round(torque_adc.max(),2)) + "Nm)" + " (min: " + str(round(torque_adc.min(),2)) + "Nm)")
# plt.plot(time,current,label="iq_motor (max: " + str(round(current.max(),2)) + "A)" + " (min: " + str(round(current.min(),2)) + "A)")
# # plt.plot(np.array(time),curr_lim,label="lim")
# # plt.plot(np.array(time),current_motor,label="τ_motor (max: " + str(round(current_motor.max(),2)) + "Nm)" + " (min: " + str(round(current_motor.min(),2)) + "Nm)")

# plt.title('Torque and Current vs Time')
# plt.ylabel('Torque [Nm] or Current [A]')
# plt.xlabel('Time [s]')
# plt.grid(True)
# plt.legend()

# plt.show()
# plt.savefig("{}_torque_plot.png".format(name))
# plt.clf()



plt.rcParams.update({'font.size': 12})
fig, axs = plt.subplots(1,2)
# I vs V
#plt1 = axs[0].scatter(counter, i_d)

#plt1 = axs[0].scatter(v_q, (i_q), s = 10, c=eff, vmin = -100, vmax = 100, cmap = 'viridis')

axs[0].scatter(v_q, i_q, s = 20, c=eff, vmin = -100, vmax = 100, cmap = 'viridis')
# axs[0].set_xlim(left = -10)
# axs[0].set_ylim(bottom = 0)
axs[0].set_ylabel('$Current$ $(A)$')
axs[0].set_xlabel('$Voltage$ $(V)$')
# T vs Vel
#axs[1].scatter(speed, (torque_adc), s = 10, c=eff, vmin = -100, vmax = 100, cmap = 'viridis')
plt1 = axs[1].scatter(speed, (torque_adc), s = 20, c=eff, cmap = 'jet')
#plt1 = axs[1].scatter(i_q,i_d)
#axs[1].scatter(vel_r_mean, torque_mean, s = 200, c=eff_r, vmin = -100, vmax = 100, cmap = 'viridis')
#axs[1].set_ylim(bottom = 0)
axs[1].set_ylabel('$Torque$ $(N-m)$')
axs[1].set_xlabel('$Velocity$ $(rad/s)$')

fig.colorbar(plt1, ax = axs, orientation = 'horizontal')
fig.suptitle('Efficiency')

plt.savefig("{}_efficiency_plot.png".format(name), dpi = 600)
plt.show()


