import json
import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

zero_deg_value = []
ninety_deg_value = []

print("""
This is for correcting the errors of servomotors.
Use your mobile phone to measure actual degrees.

--------------------------------------------------
WARNING: Disassemble the arms before testing
--------------------------------------------------
""")

if input("Continue (y/N)? ") != 'y':
    quit()

print("---0 degree test---")
for i in range(4):
    print(f"Testing the servomotor with the number: {i}")
    kit.servo[i].angle = 0
    zero_deg_value.append(int(input("Actual degree: ")))

print("---90 degree test---")
for i in range(4):
    print(f"Testing the servomotor with the number: {i}")
    kit.servo[i].angle = 90
    ninety_deg_value.append(int(input("Actual degree: ")))

error_corrections = {
    "add": [-x for x in zero_deg_value],
    "multiply": [90 / x for x in ninety_deg_value]
}

with open("error_corrections.json", "wt") as fout:
    fout.write(json.dumps(error_corrections))

for angle in range(0, 91):
    for i in range(4):
        kit.servo[i].angle = max(0, angle * error_corrections["multiply"][i] + error_corrections["add"][i])
    time.sleep(0.1)

print("Calibration is completed.")