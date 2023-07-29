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

for i in range(5):
    for j in range(4):
        """
        for angle in range(0, maximum_angle):
            for k in range(4):
                if k == j or k == (j + 1) % 4:
                    kit.servo[k].angle = 70 + calibration[k] - tension + angle
                else:
                    kit.servo[k].angle = 70 + calibration[k] - tension
            time.sleep(0.02)

        for angle in range(maximum_angle, 0, -1):
            for k in range(4):
                if k == j or k == (j + 1) % 4:
                    kit.servo[k].angle = 70 + calibration[k] - tension + angle
                else:
                    kit.servo[k].angle = 70 + calibration[k] - tension
            time.sleep(0.02)
"""

        for angle in range(0, maximum_angle):
            for k in range(4):
                if k == j:
                    kit.servo[k].angle = 70 + calibration[k] - tension + angle
                elif (k + 1) % 4 == j or k == (j + 1) % 4:
                    kit.servo[k].angle = 70 + calibration[k] - tension + angle // 2
                else:
                    kit.servo[k].angle = 70 + calibration[k] - tension
            time.sleep(0.1)

        for angle in range(maximum_angle, 0, -1):
            for k in range(4):
                if k == j:
                    kit.servo[k].angle = 70 + calibration[k] - tension + angle
                elif (k + 1) % 4 == j or k == (j + 1) % 4:
                    kit.servo[k].angle = 70 + calibration[k] - tension + angle // 2
                else:
                    kit.servo[k].angle = 70 + calibration[k] - tension
            time.sleep(0.1)


#for angle in range(90, 45, -1):
    #for i in range(4):
        #kit.servo[i].angle = angle + calibration[i]

#for angle in range(45, 90):
    #for i in range(4):
        #kit.servo[i].angle = angle + calibration[i]
