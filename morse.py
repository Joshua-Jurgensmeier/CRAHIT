#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# Definitions adapted from https://en.wikipedia.org/Morse_code

# The length of a dot (also called "dit") and the separator between 
# parts of the same letter are one unit
dit = 1
# A dash (also called "dah") and the separator between letters are three units
dah = 3 * dit   
# The space between words is seven units
space = 7 * dit
# (For this program) the end of a message is signaled by holding for 5 seconds
stop = 5 * dit

# A dictionary that maps English letter -> Morse code 
# Google "python dictionary"
# Or just accept it as magic for now. It is only used in the decode function.
letter2morse = { 'A':'.-', 'B':'-...', 
                    'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 
                    'I':'..', 'J':'.---', 'K':'-.-', 
                    'L':'.-..', 'M':'--', 'N':'-.', 
                    'O':'---', 'P':'.--.', 'Q':'--.-', 
                    'R':'.-.', 'S':'...', 'T':'-', 
                    'U':'..-', 'V':'...-', 'W':'.--', 
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
                    '1':'.----', '2':'..---', '3':'...--', 
                    '4':'....-', '5':'.....', '6':'-....', 
                    '7':'--...', '8':'---..', '9':'----.', 
                    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
                    '?':'..--..', '/':'-..-.', '-':'-....-', 
                    '(':'-.--.', ')':'-.--.-'}

# A very confusing and magical line.
# It reverses the letter2morse dictionary.
# morse2letter maps Morse code -> English letter
# Accept as magic, or Google "python dictionary comprehension"
morse2letter = {v: k for k, v in letter2morse.items()}

# setup pins
BTN = 11
LED = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT)

# Waits until the user sends the stop code (hold for 5 units).
# Returns a list representing the history of button state changes.
# The first element is the length in seconds of the first press, 
# and the second is the length of the first release, etc.
# Example return:
# delay_list:  [1.124124, 0.91242, 3.12243, 3.59099, 2.93728, 7.1937, 1.2234, 0.72434]
def listen_for_delays():
    # Wait for first press
    while not GPIO.input(BTN):
        pass
    
    # Init vars
    delay_list = []
    should_stop = False
    # Keeps track of the last button state we saw.
    # We'll only check the button every 0.1 seconds.
    # True is pressed.
    last_btn_state = True
    t0 = time.time() # Start timer

    # Listen
    while not should_stop:
        delay = time.time()-t0 # Update timer
        btn_state = GPIO.input(BTN) # Check button
        # Detect state change (e.g. pressed -> released)
        if(last_btn_state != btn_state):
            last_btn_state = btn_state
            # Save delay between toggles
            delay_list.append(delay)
            # Reset timer
            t0 = time.time()
        # Check for stop code
        elif(delay > stop and btn_state == True):
            should_stop = True
        
        # Why loop around at nanosecond speed, when you can race
        # around in deciseconds!
        time.sleep(0.1)
    
    # Remove the released delay between the last letter and stop code
    delay_list.pop()
    
    return delay_list

# Decodes the passed in list of state change time delays
# into a list of strings of dits and dahs.
# Words are separate strings, letters are seperated by slashes
# (See unit definitions at top of file)
# Example argument and return:

# Btn state:   down       up       down     up       down     up      down    up
# delay_list:  [1.124124, 0.91242, 3.12243, 3.59099, 2.93728, 7.1937, 1.2234, 0.72434]
# Description: dit        sep      dah      ltr-sep  dah      space   dit     sep
# word_list:   [".-/-", "."]
# English:        at     e
def interpret_delays(delay_list):
    # The delays alternate between "up" delays and "down" delays
    # isPressed flips between True and False every loop
    isPressed = True
    # The list that will be filled with encoded words 
    word_list = []
    # A string used to build encoded words
    word = ""

    # For each delay, figure out what it is.
    for delay in delay_list:
        # "down" delay. Button is pressed.
        if isPressed:
            # Dit
            if delay <= (dit + dah)/2:
                word += "."
            # Dah
            else: # delay > (dit + dah)/2 and delay < 5
                word += "-"
        # "up" delay. Button is release.
        else:
            # If delay is a space. Threshold is average of dah and space.
            if delay > (dah + space)/2: 
                # Add word to list
                word_list.append(word)
                # reset for next word
                word = ""
            # If delay is a letter separator. (greater than dit, less than space)
            elif delay > (dah + dit)/2 and delay <= (dah + space)/2:
                # Add a slash character, indicating letter seperator
                word += "/"
            # Else delay is a letter part separator
                # Do nothing
        # Negate isPressed: True -> False; False -> True
        isPressed = not isPressed
    # Add on last word
    word_list.append(word)
    return word_list

# Decodes a list of dit dah strings into letters and words
# returns one string.
# Example argument and return:
# word_list: [".-/-", "."]
# return:    "AT E"
def decode(word_list):
    message = ""
    for word in word_list:
        # Splits the word into a list of letters
        # Google "python split"
        letter_list = word.split(sep="/")
        for letter in letter_list:
            message += morse2letter[letter]
        
        message += " "
        
    return message


def main():
    # Print welcome/instructions
    print("Enter message in Morse Code. Hold button for 5 seconds to end message.")
    print("Dit is " + str(dit) + " seconds.")

    # Listen
    delay_list = listen_for_delays()
    print(delay_list)

    # Decode
    code_list = interpret_delays(delay_list)
    print(code_list)
    message = decode(code_list)
    
    # Print results
    print("I heard:")
    print(message)

    GPIO.cleanup()

main()