from matplotlib import pyplot as plt
import csv
import numpy as np
import pandas as pd

frequency = 200
hold_time = 1.0
name = "Efficiency_1682187335.7867422.csv"

data = pd.read_csv(name)

time_raw = np.array(data['loop time'])
D1_vel_raw = np.array(data['Output Velocity D1'])
futek_torque_raw = -1.0*np.array(data['Futek Torque'])
D1_VBus_raw = np.array(data['V_BUS D1'])
D1_IBus_raw = np.array(data['I_Bus D1'])
D1_Vq_raw = np.array(data['V_q D1'])
D1_Iq_raw = np.array(data['I_q D1'])
D1_Vd_raw = np.array(data['V_d D1'])
D1_Id_raw = np.array(data['I_d D1'])
D2_vel_raw = np.array(data['Output Velocity D2'])
D2_VBus_raw = np.array(data['V_BUS D2'])
D2_IBus_raw = np.array(data['I_Bus D2'])
D2_Vq_raw = np.array(data['V_q D2'])
D2_Iq_raw = np.array(data['I_q D2'])
D2_Vd_raw = np.array(data['V_d D2'])
D2_Id_raw = np.array(data['I_d D2'])
max_vel_raw = np.array(data['max_velocity'])
max_curr_raw = np.array(data['max_current'])

numer_points = int(frequency*hold_time)
number_samples = int(time_raw.size/(numer_points))
print("numer_points: ",numer_points)
print("number_samples: ",number_samples)

D1_vel = np.array([])
futek_torque = np.array([])
D1_VBus = np.array([])
D1_IBus = np.array([])
D1_Vq = np.array([])
D1_Iq = np.array([])
D1_Vd = np.array([])
D1_Id = np.array([])
D2_vel = np.array([])
D2_VBus = np.array([])
D2_IBus = np.array([])
D2_Vq = np.array([])
D2_Iq = np.array([])
D2_Vd = np.array([])
D2_Id = np.array([])
max_vel = np.array([])
max_curr = np.array([])


#print(time_raw[0:numer_points].size)
for i in range(0,number_samples):
    D1_vel = np.append(D1_vel,np.mean(D1_vel_raw[i*numer_points:(i*numer_points)+numer_points]))
    futek_torque = np.append(futek_torque,np.mean(futek_torque_raw[i*numer_points:(i*numer_points)+numer_points]))
    D1_VBus = np.append(D1_VBus,np.mean(D1_VBus_raw[i*numer_points:(i*numer_points)+numer_points]))
    D1_IBus = np.append(D1_IBus,np.mean(D1_IBus_raw[i*numer_points:(i*numer_points)+numer_points]))
    D1_Vq = np.append(D1_Vq,np.mean(D1_Vq_raw[i*numer_points:(i*numer_points)+numer_points]))
    D1_Iq = np.append(D1_Iq,np.mean(D1_Iq_raw[i*numer_points:(i*numer_points)+numer_points]))
    D1_Vd = np.append(D1_Vd,np.mean(D1_Vd_raw[i*numer_points:(i*numer_points)+numer_points]))
    D1_Id = np.append(D1_Id,np.mean(D1_Id_raw[i*numer_points:(i*numer_points)+numer_points]))
    D2_vel = np.append(D2_vel,np.mean(D2_vel_raw[i*numer_points:(i*numer_points)+numer_points]))
    D2_VBus = np.append(D2_VBus,np.mean(D2_VBus_raw[i*numer_points:(i*numer_points)+numer_points]))
    D2_IBus = np.append(D2_IBus,np.mean(D2_IBus_raw[i*numer_points:(i*numer_points)+numer_points]))
    D2_Vq = np.append(D2_Vq,np.mean(D2_Vq_raw[i*numer_points:(i*numer_points)+numer_points]))
    D2_Iq = np.append(D2_Iq,np.mean(D2_Iq_raw[i*numer_points:(i*numer_points)+numer_points]))
    D2_Vd = np.append(D2_Vd,np.mean(D2_Vd_raw[i*numer_points:(i*numer_points)+numer_points]))
    D2_Id = np.append(D2_Id,np.mean(D2_Id_raw[i*numer_points:(i*numer_points)+numer_points]))
    max_vel = np.append(max_vel,np.mean(max_vel_raw[i*numer_points:(i*numer_points)+numer_points]))
    max_curr = np.append(max_curr,np.mean(max_curr_raw[i*numer_points:(i*numer_points)+numer_points]))
    

Power_Mech_1 = D1_vel*futek_torque
Power_Mech_2 = D2_vel*futek_torque

Power_ElecM_1 = D1_Vq*D1_Iq
Power_ElecM_2 = D2_Vq*D2_Iq

Power_ElecB_1 = D1_IBus*D1_VBus
Power_ElecB_2 = D2_IBus*D2_VBus

eff_d1 = np.zeros_like(Power_Mech_1)
eff_d2 = np.zeros_like(Power_Mech_2)



for i in range(Power_Mech_1.shape[0]):
    # Efficiency
    if D1_vel[i] >0:
        Eff_driver1 = Power_ElecM_1[i]/Power_ElecB_1[i]
        Eff_driver2 = Power_ElecB_2[i]/Power_ElecM_2[i]
        
        Eff_Motor1 = Power_Mech_1[i]/Power_ElecM_1[i]
        Eff_Motor2 = Power_ElecM_2[i]/Power_Mech_2[i]
        
        Eff_All1 = Power_Mech_1[i]/Power_ElecB_1[i]
        Eff_All2 = Power_ElecB_2[i]/Power_Mech_2[i]
        
    else:
        Eff_driver1 = Power_ElecB_1[i]/Power_ElecM_1[i]
        Eff_driver2 = Power_ElecM_2[i]/Power_ElecB_2[i]
        
        Eff_Motor1 = Power_ElecM_1[i]/Power_Mech_1[i]
        Eff_Motor2 = Power_Mech_2[i]/Power_ElecM_2[i]
        
        Eff_All1 = Power_ElecB_1[i]/Power_Mech_1[i]
        Eff_All2 = Power_Mech_2[i]/Power_ElecB_2[i]    
    

    tmp_d1 = Eff_All1*100.0
    tmp_d2 = Eff_All2*100.0
    if(tmp_d1 < -100):
        print(tmp_d1)
    eff_d1[i] = tmp_d1 if ((not np.isnan(tmp_d1) and not np.isinf(tmp_d1))) else -100
    eff_d2[i] = tmp_d2 if ((not np.isnan(tmp_d2) and not np.isinf(tmp_d2))) else -100

D1_vel = np.append(D1_vel,D2_vel)
futek_torque = np.append(futek_torque,futek_torque)
eff_d1 = np.append(eff_d1,eff_d2)
D1_Vq = np.append(D1_Vq,D2_Vq)
D1_Iq = np.append(D1_Iq,D2_Iq)
D1_VBus = np.append(D1_VBus,-D1_VBus)
D1_IBus = np.append(D1_IBus, D1_IBus)




plt.rcParams.update({'font.size': 12})
fig, axs = plt.subplots(1,2)

# Iq vs Vq
axs[0].scatter(D1_Vq, D1_Iq, s = 20, c=eff_d1, vmax=100, vmin=-100, cmap = 'viridis')
axs[0].set_ylabel('$Current$ $(A)$')
axs[0].set_xlabel('$Voltage$ $(V)$')

# T vs Vel
plt1 = axs[1].scatter(D1_vel, futek_torque, s = 20, c=eff_d1,vmax=100, vmin=-100, cmap = 'viridis')
axs[1].set_ylabel('$Torque$ $(N-m)$')
axs[1].set_xlabel('$Velocity$ $(rad/s)$')

fig.colorbar(plt1, ax = axs, orientation = 'horizontal')
fig.suptitle('Efficiency')

plt.savefig("{}_efficiency_plot.png".format(name), dpi = 600)
plt.show()
