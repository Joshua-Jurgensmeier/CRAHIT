import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)

GPIO.setmode(GPIO.BOARD)
led = 13
btn = 11

GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(led, GPIO.OUT)

templateData = {
        "btn": btn,
        "led": led,
        "btn_state": 0,
        "led_state": 0
    }

@app.route("/")
def root():
    GPIO.output(led, GPIO.LOW)
    return "Go to /1"

@app.route("/<int(min=0, max=1):state>")
def ledState(state):

    GPIO.output(led, state)

    templateData["led_state"] = state
    templateData["btn_state"] = GPIO.input(btn)

    # Push our values out to the template, generate html, and then send it to client
    return render_template('./btnled.html', **templateData)

app.run(host="0.0.0.0", port=80, debug=True)