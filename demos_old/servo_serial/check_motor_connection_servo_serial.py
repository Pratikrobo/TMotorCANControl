from TMotorCANControl.servo_serial import TMotorManager_servo_serial

# CHANGE THESE TO MATCH YOUR DEVICE!
Type = 'AK80-9'
ID = 41

with TMotorManager_servo_serial(motor_type=Type) as dev:
    if dev.check_connection():
        print("\nmotor is successfully connected!\n")
    else:
        print("\nmotor not connected. Check dev power, network wiring, and Serial bus connection.\n")
    