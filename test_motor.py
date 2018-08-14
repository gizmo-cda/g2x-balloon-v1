#!/usr/bin/env python3

import os
import sys
import time
import atexit
import RPi.GPIO as GPIO

# configuraion
MOTOR_0 = (12, 13)   # direction, drive
MOTOR_1 = (16, 18)

DIRECTION = 0
DRIVE = 1

MS = 0.001
PULSE_TIME = 0.33 * MS
WAIT_TIME = PULSE_TIME

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOTOR_0[0], GPIO.OUT)
    GPIO.setup(MOTOR_0[1], GPIO.OUT)
    GPIO.setup(MOTOR_1[0], GPIO.OUT)
    GPIO.setup(MOTOR_1[1], GPIO.OUT)


def shutdown():
    GPIO.cleanup([MOTOR_0[0], MOTOR_0[1], MOTOR_1[0], MOTOR_1[1]])
    print("shutdown")


def revolve(direction):
    for _ in range(0, 2048):
        GPIO.output(MOTOR_0[DIRECTION], direction)
        GPIO.output(MOTOR_1[DIRECTION], direction)

        GPIO.output(MOTOR_0[DRIVE], True)
        GPIO.output(MOTOR_1[DRIVE], True)
        time.sleep(PULSE_TIME)

        GPIO.output(MOTOR_0[DRIVE], False)
        GPIO.output(MOTOR_1[DRIVE], False)
        time.sleep(WAIT_TIME)


if __name__ == "__main__":
    if os.geteuid() != 0:
        print("You must run this script using root privileges")
        sys.exit(1)

    atexit.register(shutdown)

    init_gpio()

    revolve(False)
    revolve(True)
    
