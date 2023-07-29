import adafruit_mpu6050
import board
import time
from math import sin, cos, atan, pi, degrees, radians
from PID import PID
from servo_controller import set_angle_for_plate
from sensor_controller import calibrate_sensor, get_angle
from periodic_sleeper import PeriodicSleeper

i2c = board.I2C()
mpu = adafruit_mpu6050.MPU6050(i2c)

theta = 0.  # angle on XZ, 3 to 1
phi = 0.  # angle on YZ, 4 to 2

kp, ki, kd = 0.015, 0.015, 0.0003

theta_pid = PID(kp, ki, kd)
phi_pid = PID(kp, ki, kd)

def balance_plate():
    """
    Balance the plate with PID control.
    """

    global theta, phi, theta_pid, phi_pid

    theta_err, phi_err = get_angle()

    theta += theta_pid.generate(-theta_err)
    phi += phi_pid.generate(-phi_err)

    #if theta > radians(30):
        #theta = radians(30)

    #if phi > radians(30):
        #phi = radians(30)

    try:
        set_angle_for_plate(theta, phi)
    except ValueError:
        pass


if __name__ == '__main__':

    set_angle_for_plate(0, 0)

    time.sleep(0.5)
    print("Calibrating the board... ", end='')
    calibrate_sensor()
    print("Done!")

    sleeper = PeriodicSleeper(balance_plate, 0.01)

    while True:
        try:
            kp, ki, kd = map(float, input("New kp, ki kd: ").split())

            theta_pid = PID(kp, ki, kd)
            phi_pid = PID(kp, ki, kd)

        except ValueError:
            print("Invalid value")
