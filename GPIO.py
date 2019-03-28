#!/usr/bin/python3
import RPi.GPIO as GPIO
import time


# Setup
LED = 13
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)

# Main
for i in range(20):
    GPIO.output(LED, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(LED, GPIO.LOW)
    time.sleep(0.5)

# GPIO.output(LED, GPIO.LOW)
# time.sleep(3)
# Cleanup
GPIO.cleanup()
