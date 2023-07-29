import adafruit_mpu6050
import board
import time
from math import sin, cos, atan, pi, radians
from servo_controller import set_angle_for_plate

acel_deadzone = 0.005
gyro_deadzone = 0.0005
grav_acel = 9.5
buff_size = 100
complementry_alpha = 0.96

acel_offset = [0.0, 0.0, 0.0]
gyro_offset = [0.0, 0.0, 0.0]

i2c = board.I2C()
mpu = adafruit_mpu6050.MPU6050(i2c)
prev_angle = [0.0, 0.0, 0.0]
prev_time = 0.0


def calibrate_sensor():
    """
    Calibrate the sensor and store the correction data.
    """

    while True:
        acel_mean = [0.0, 0.0, 0.0]
        gyro_mean = [0.0, 0.0, 0.0]

        for i in range(buff_size):
            acel_mean = [
                x + y + z for x, y, z in zip(acel_mean, mpu.acceleration, acel_offset)
            ]
            gyro_mean = [x + y + z for x, y, z in zip(gyro_mean, mpu.gyro, gyro_offset)]
            time.sleep(0.001)

        acel_mean = [x / buff_size for x in acel_mean]
        gyro_mean = [x / buff_size for x in gyro_mean]

        acel_mean[2] += grav_acel

        flag = True

        for i in range(3):
            if abs(acel_mean[i]) > acel_deadzone:
                acel_offset[i] = acel_offset[i] - acel_mean[i] / 2
                flag = False
            if abs(gyro_mean[i]) > gyro_deadzone:
                gyro_offset[i] = gyro_offset[i] - gyro_mean[i] / 2
                flag = False

        if flag:
            break


def get_acceleration():
    """
    Return the acceleration (calibrated).

    :return: a tuple of acceleration.
    """
    return tuple([x + y for x, y in zip(mpu.acceleration, acel_offset)])


def get_gyro():
    """
    Return the gyro (calibrated).

    :return: a tuple of gyro.
    """
    return tuple([x + y for x, y in zip(mpu.gyro, gyro_offset)])


def get_angle():
    """
    Return an angle after applying the complementry filter.

    :return: a tuple of theta and phi in radian.
    """

    global prev_angle
    global prev_time

    if prev_time == 0:
        prev_time = time.time()

    cur_time = time.time()
    sample_time = cur_time - prev_time
    prev_time = cur_time

    acel = get_acceleration()
    gyro = get_gyro()

    # cur_angle = [atan(acel[0] / acel[2]), atan(acel[1] / acel[2])]

    cur_angle = []

    # X to Z
    acel_angle = atan(acel[0] / acel[2])
    gyro_angle = -radians(float(gyro[1]) * sample_time)
    cur_angle.append(
        complementry_alpha * (gyro_angle + prev_angle[0])
        + (1 - complementry_alpha) * acel_angle
    )

    # Y to Z
    acel_angle = atan(acel[1] / acel[2])
    gyro_angle = radians(float(gyro[0]) * sample_time)
    cur_angle.append(
        complementry_alpha * (gyro_angle + prev_angle[1])
        + (1 - complementry_alpha) * acel_angle
    )

    prev_angle = cur_angle

    # Convert it to theta and phi
    a, b = cur_angle

    theta = atan((sin(a) + sin(b)) / ((cos(a) ** 2 + cos(b) ** 2) ** (1 / 2)))
    phi = atan((-sin(a) + sin(b)) / ((cos(a) ** 2 + cos(b) ** 2) ** (1 / 2)))

    return theta, phi


if __name__ == "__main__":
    from servo_controller import set_angle_for_plate

    set_angle_for_plate(0, 0)
    # calibrate_sensor()
    print("acel_offset: ", acel_offset)
    print("gyro_offset: ", gyro_offset)

    from periodic_sleeper import PeriodicSleeper

    sleeper = PeriodicSleeper(get_angle, 0.005)

    while True:
        from math import degrees

        print(degrees(prev_angle[0]), degrees(prev_angle[1]))
        time.sleep(1)
