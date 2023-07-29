import json
import time
import sys
from cmath import exp, log
from math import degrees, radians
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
kit.servo[0].set_pulse_width_range(500, 2500)
kit.servo[1].set_pulse_width_range(500, 2500)
kit.servo[2].set_pulse_width_range(500, 2500)
kit.servo[3].set_pulse_width_range(500, 2500)

MIN_ANGLE = 45
MAX_ANGLE = 130

try:
    with open("error_corrections.json", "rt") as fin:
        ec = json.loads(fin.read())
except OSError:
    print("Could not read the calibration file.", file=sys.stderr)
    quit()


def set_angle_for_servomotor(channel, angle):
    """
    It is for setting the calibrated angle of a specified servomotor.

    :param channel: specifies the servomotor
    :param angle: specified the angle
    :return: nothing
    :raise ValueError: when the invalid channel or angle is given.
    """

    if not (MIN_ANGLE < angle < MAX_ANGLE and 0 <= channel <= 3):
        raise ValueError(
            f"Angle must be between {MIN_ANGLE} and {MAX_ANGLE}, but got {angle}"
        )

    kit.servo[channel].angle = angle * ec["multiply"][channel] + ec["add"][channel]


def set_angle_for_plate(theta, phi):
    """
    It sets the angles of the plate.

    :param theta: angle on the line from the servomotor 3 to 1 in radian.
    :param phi: angle on the line from the servomotor 4 to 2 in radian.
    :return: nothing
    """

    # Some magic going on here...
    def calc(theta):
        a = 8  # bottom arm
        b = 5.3  # top arm
        c = 5.7  # the distance from the center to the origin of the bottom arm rotation
        r = 5.7  # the distance from the center to the attached point on the top plate
        h = 12  # the height of the plate
        res = degrees(
            (
                -log(
                    -(
                        -c * r
                        + h * r * 1j
                        + a**2 * exp(theta * 1j)
                        - b**2 * exp(theta * 1j)
                        + c**2 * exp(theta * 1j)
                        + h**2 * exp(theta * 1j)
                        + r**2 * exp(theta * 1j)
                        + (
                            4
                            * (
                                -a * r
                                + a * c * exp(theta * 1j)
                                + a * h * exp(theta * 1j) * 1j
                            )
                            * (
                                -a * c * exp(theta * 1j)
                                + a * h * exp(theta * 1j) * 1j
                                + a * r * exp(theta * 2j)
                            )
                            + (
                                -c * r
                                + h * r * 1j
                                + a**2 * exp(theta * 1j)
                                - b**2 * exp(theta * 1j)
                                + c**2 * exp(theta * 1j)
                                + h**2 * exp(theta * 1j)
                                + r**2 * exp(theta * 1j)
                                - c * r * exp(theta * 2j)
                                - h * r * exp(theta * 2j) * 1j
                            )
                            ** 2
                        )
                        ** (1 / 2)
                        - c * r * exp(theta * 2j)
                        - h * r * exp(theta * 2j) * 1j
                    )
                    / (
                        2
                        * (
                            -a * r
                            + a * c * exp(theta * 1j)
                            + a * h * exp(theta * 1j) * 1j
                        )
                    )
                )
                * 1j
            ).real
        )

        if res > 90:
            return 180 - res

        return res

    set_angle_for_servomotor(0, calc(theta))
    set_angle_for_servomotor(1, calc(phi))
    set_angle_for_servomotor(2, calc(-theta))
    set_angle_for_servomotor(3, calc(-phi))


if __name__ == "__main__":
    set_angle_for_plate(radians(0), radians(0))
