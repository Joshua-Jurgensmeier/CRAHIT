#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# Initialization
red = 15
green = 13
blue = 16

rgb = [red, green, blue]

GPIO.setmode(GPIO.BOARD)
GPIO.setup(rgb, GPIO.OUT)


def make_blue():
    GPIO.output(red, 0)
    GPIO.output(green, 0)
    GPIO.output(blue, 1)
    # Or just
    # GPIO.output(rgb, [0,0,1])


def permute():
    colors = [0, 0, 0]
    for i in [0, 1]:
        colors[0] = i
        for j in [0, 1]:
            colors[1] = j
            for k in [0, 1]:
                colors[2] = k
                print(colors)
                GPIO.output(rgb, colors)
                time.sleep(1)

make_blue()
time.sleep(3)

#permute()

GPIO.output(rgb, [1, 0, 1])
time.sleep(1)

# GPIO.output(rgb, [1, 0, 0])
# time.sleep(1)
# GPIO.output(rgb, [0, 1, 0])
# time.sleep(1)
# GPIO.output(rgb, [0, 0, 1])
# time.sleep(1)

GPIO.cleanup()