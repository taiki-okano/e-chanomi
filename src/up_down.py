# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for a standard servo on channel 0 and a continuous rotation servo on 
channel 1."""

import time
from adafruit_servokit import ServoKit


# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)

maximum_angle = 30
tension = 55
calibration = [34, 18, 18, 34]

for angle in range(maximum_angle):
    kit.servo[0].angle = 15 + calibration[0] + angle
    kit.servo[1].angle = 15 + calibration[1] + angle
    kit.servo[2].angle = 15 + calibration[2] - angle
    kit.servo[3].angle = 15 + calibration[3] - angle
    time.sleep(0.1)
