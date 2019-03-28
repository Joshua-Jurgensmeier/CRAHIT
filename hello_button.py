#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

BTN = 11
# LED = 

# setup pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Waiting...")
# do stuff
while not GPIO.input(BTN):
    pass

print("Hello button!")

GPIO.cleanup()