# * Updated version: https://github.com/EloiStree/License
# * ----------------------------------------------------------------------------
# */

######## PRINT BASIC INFO OF THE DEVICE ########
import sys
print("Hello World")
print(f"sys.implementation: {sys.implementation}")
print(f"sys.version: {sys.version}")
print(f"sys.platform: {sys.platform}")


import time
import board
import busio
import pulseio
import analogio
import random
import struct
import digitalio
import usb_hid
import usb_midi
import adafruit_midi
import time
import ssl
import socketpool
import wifi
import adafruit_requests
import os
import ipaddress


# IMPORT FROM NEAR FILE
from hid_gamepad import Gamepad
from wow_int import WowInt
from hc_ttl import HCTTL
from bluetooth_electronics_builder import BluetoothElectronicsBuilder

# IMPORT FROM LIB ADAFRUIT
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
#from keyboard_layout_fr import KeyboardLayoutFR  # Import the French layout
from adafruit_hid.mouse import Mouse
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode



# 🐿️ If gamepad is not found in usb_hid.devices
# Just reboot the device in boot mode and comeback.
gamepad= Gamepad(usb_hid.devices)           # Start behaving as gamepad
mouse  = Mouse(usb_hid.devices)             # Start behaving as mouse
consumer = ConsumerControl(usb_hid.devices) # Start behaving as media control
keyboard = Keyboard(usb_hid.devices)
midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1], in_channel=0, out_channel=0)

pin8 = digitalio.DigitalInOut(board.GP8)
pin8.direction = digitalio.Direction.INPUT
pin8.pull = digitalio.Pull.UP

pin10 = digitalio.DigitalInOut(board.GP10)
pin10.direction = digitalio.Direction.INPUT
pin10.pull = digitalio.Pull.UP

pin12 = digitalio.DigitalInOut(board.GP12)
pin12.direction = digitalio.Direction.INPUT
pin12.pull = digitalio.Pull.UP

pin21 = digitalio.DigitalInOut(board.GP21)
pin21.direction = digitalio.Direction.INPUT
pin21.pull = digitalio.Pull.UP

pin20 = digitalio.DigitalInOut(board.GP20)
pin20.direction = digitalio.Direction.INPUT
pin20.pull = digitalio.Pull.UP

pin19 = digitalio.DigitalInOut(board.GP19)
pin19.direction = digitalio.Direction.INPUT
pin19.pull = digitalio.Pull.UP

pin18 = digitalio.DigitalInOut(board.GP18)
pin18.direction = digitalio.Direction.INPUT
pin18.pull = digitalio.Pull.UP

while True:
    if(pin8.value):
        gamepad.press_buttons(8)
    else :
        gamepad.release_buttons(8)
    if(pin10.value):
        gamepad.press_buttons(10)
    else :
        gamepad.release_buttons(10) 
    if(pin12.value):
        gamepad.press_buttons(12)
    else :
        gamepad.release_buttons(12)
    if( not pin18.value):
        gamepad.press_buttons(18)
    else :
        gamepad.release_buttons(18)
    if(not pin19.value):
        gamepad.press_buttons(19)
    else :
        gamepad.release_buttons(19)
    if(not pin20.value):
        gamepad.press_buttons(20)
    else :
        gamepad.release_buttons(20)
    if(not pin21.value):
        gamepad.press_buttons(21)
    else :
        gamepad.release_buttons(21)
        
    time.sleep(0.1)
        #gamepad.set_joystick_left_x_percent(random.randrange(-100,100)/100.0)
        #gamepad.set_joystick_left_y_percent(random.randrange(-100,100)/100.0)
        #gamepad.set_joystick_right_x_percent(random.randrange(-100,100)/100.0)
        #gamepad.set_joystick_right_y_percent(random.randrange(-100,100)/100.0)
        #gamepad.set_trigger_left_percent(random.randrange(0,100)/100.0)
        #gamepad.set_trigger_right_percent(random.randrange(0,100)/100.0)
        #button_index= random.randint(1,15)
        #gamepad.press_buttons(button_index)
    
        #time.sleep(1)
        #gamepad.release_buttons(button_index)
        #time.sleep(1)



        