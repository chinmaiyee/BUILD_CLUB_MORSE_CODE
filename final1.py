import RPi.GPIO as GPIO
from time import time, sleep
import keyboard
# Time constants
dot_duration = 0.2  # Time for a dot (.)
dash_duration = 0.5  # Time for a dash (-)
space_duration = 1.0  # Time for a space between words
end_gap = 2.0  # Time gap for end of message

# Create a dictionary of Morse Code
MorseCodes = {
    ' ': '',
    'a': 'sl',
    'b': 'lsss',
    'c': 'lsls',
    'd': 'lss',
    'e': 's',
    'f': 'ssls',
    'g': 'lls',
    'h': 'ssss',
    'i': 'ss',
    'j': 'slll',
    'k': 'lsl',
    'l': 'slss',
    'm': 'll',
    'n': 'ls',
    'o': 'lll',
    'p': 'slls',
    'q': 'llsl',
    'r': 'sls',
    's': 'sss',
    't': 'l',
    'u': 'ssl',
    'v': 'sssl',
    'w': 'sll',
    'x': 'lssl',
    'y': 'lsll',
    'z': 'llss',
    '1': 'sllll',
    '2': 'sslll',
    '3': 'sssll',
    '4': 'ssssl',
    '5': 'sssss',
    '6': 'lssss',
    '7': 'llsss',
    '8': 'lllss',
    '9': 'lllls',
    '0': 'lllll'
}

# Set up GPIO mode (using BOARD pin numbering)
GPIO.setmode(GPIO.BOARD)

# Pins setup
shortled_pin = 8  # Physical pin 8
longled_pin = 10  # Physical pin 10 (you can use the same pin if needed)

# Set pins
GPIO.setup(shortled_pin, GPIO.OUT)
GPIO.setup(longled_pin, GPIO.OUT)

# Time for fast and slow blinks
fast = 0.1
slow = 0.2

# Flags for light
light = True

# Pin states (Initial state)
GPIO.output(shortled_pin, GPIO.LOW)
GPIO.output(longled_pin, GPIO.LOW)

def letterlookup(stringvalue):
    for k in MorseCodes:
        if MorseCodes[k] == stringvalue:
            return k
    return " "

def blinkletter(letter):
    if letter != "":
        currentletter = MorseCodes[letter]
    if letter == " ":
        sleep(0.6)
        return
    
    print(letter + " : " + currentletter)
    for c in currentletter:
        if c == 'l':
            blinkspeed = slow
        if c == 's':
            blinkspeed = fast
        
        if light: 
            GPIO.output(shortled_pin, GPIO.HIGH)  # Turn on LED for short
        sleep(blinkspeed)
        
        if light:
            GPIO.output(shortled_pin, GPIO.LOW)  # Turn off LED
        sleep(blinkspeed)
    
    sleep(0.6)

def playmessage(message):           
    for c in message:
        blinkletter(str.lower(c))

# Test the message
#playmessage("hello world")
# Function to detect key press duration and classify the input
def detect_space_press():
    press_start = None
    while True:
        if keyboard.is_pressed('space'):  # If space key is pressed
            if press_start is None:  # Record the start time when key is pressed
                press_start = time()
        elif press_start is not None:  # When space key is released
            press_duration = time() - press_start  # Calculate the duration of the press
            press_start = None  # Reset press_start

            if press_duration < dot_duration:
                return "Dot"
            elif press_duration < dash_duration:
                return "Dash"
            elif press_duration < space_duration:
                return "Space"
            elif press_duration > end_gap:
                return "End"

        sleep(0.01)  # Small sleep to avoid busy-waiting

# Function to process Morse code input
def process_morse_input():
    morse_message = []
    print("Press and hold the space bar for dot, dash, or word space...")
    
    while True:
        result = detect_space_press()
        
        if result == "End":
            print("End of message detected.")
            break  # End after 2-second gap
        
        print(f"Detected: {result}")
        morse_message.append(result)
        
        # Optionally print out the current morse message so far
        print("Current Morse: ", morse_message)

    print("Final Morse Message: ", morse_message)
    return morse_message

# Function to decode Morse code into text
def decode_morse(morse_message):
    decoded_message = []
    current_letter = ""
    
    for item in morse_message:
        if item == "Dot":
            current_letter += "s"
        elif item == "Dash":
            current_letter += "l"
        elif item == "Space":  # Space between letters
            if current_letter:
                decoded_message.append(letter_from_morse(current_letter))
                current_letter = ""
        elif item == "End":  # End of message
            if current_letter:
                decoded_message.append(letter_from_morse(current_letter))
            break
    
    # After processing, add the last letter if any
    if current_letter:
        decoded_message.append(letter_from_morse(current_letter))

    decoded_message = ' '.join(decoded_message)  # Join decoded words
    print(f"Decoded Message: {decoded_message}")
    return decoded_message

# Function to look up letter from Morse code
def letter_from_morse(morse_code):
    for letter, code in MorseCodes.items():
        if code == morse_code:
            return letter
    return '?'  # If not found, return '?' for unknown code

# Run the Morse input detection and decoding
morse_input = process_morse_input()
#decode_morse(morse_input)
sleep(0.01)
playmessage(decode_morse(morse_input))

# Cleanup GPIO at the end
GPIO.cleanup()
