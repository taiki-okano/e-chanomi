import wheels
import time
import balancer
import servo_controller
import sensor_controller
import periodic_sleeper
import keyboard

SPEED = 55

if __name__ == "__main__":
    servo_controller.set_angle_for_plate(0, 0)

    input("Place it to the horizontal place (Enter to conitnue)")

    print("Calibrating the board... ")

    sensor_controller.calibrate_sensor()

    print("Done!")

    balancer = periodic_sleeper.PeriodicSleeper(balancer.balance_plate, 0.01)

    # wheels.setup()

    # while True:
    #     if keyboard.is_pressed("w"):
    #         wheels.motor_left(1, 1, SPEED)
    #         wheels.motor_right(1, 0, SPEED)
    #         time.sleep(1)
    #     elif keyboard.is_pressed("s"):
    #         wheels.motor_left(1, 0, SPEED)
    #         wheels.motor_right(1, 1, SPEED)
    #         time.sleep(1)
    #     elif keyboard.is_pressed("a"):
    #         wheels.motor_left(1, 1, SPEED)
    #         wheels.motor_right(1, 1, SPEED)
    #         time.sleep(1)
    #     elif keyboard.is_pressed("d"):
    #         wheels.motor_left(1, 0, SPEED)
    #         wheels.motor_right(1, 0, SPEED)
    #         time.sleep(1)
