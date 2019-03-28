#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import random

BTN = 11
LED = 13
timeout = 5

# setup pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT)

def wait_for_press():
    while not GPIO.input(BTN):
        time.sleep(0.2)
    time.sleep(0.2)


def wait_for_release():
    while GPIO.input(BTN):
        time.sleep(0.2)
    time.sleep(0.2)

def count_presses(timeout):
    t0 = time.time()
    press_count = 0
    while(time.time() - t0 < timeout):
        if GPIO.input(BTN):
            press_count += 1
            wait_for_release()

    return press_count

def blinkn(n):
    for i in range(n):
        GPIO.output(LED, 1)
        time.sleep(1)
        GPIO.output(LED, 0)
        time.sleep(1)

def main():
    playing = True
    while playing:
        # Say
        print("Simon says:")
        times = random.randint(1, 5)
        blinkn(times)
        # Listen
        print("You have 5 seconds!")
        answer = count_presses(timeout)
        # Report result
        if(answer == times):
            print("Correct!!")
        else:
            print("Incorrect!!")
        # Play again?
        playing = input("Press just ENTER to play again. Type anything else to quit: ") == ""
    GPIO.cleanup()
main()