# * Updated version: https://github.com/EloiStree/License
# * ----------------------------------------------------------------------------
# */


""" FOOT BOARD ON A PICO W Terminal connections:
0 RX TX TTL
1 RX TX TTL
2 Audio Jack 3.5mm white Cable
3 Audio Jack 3.5mm red Cable
4 Audio Jack 3.5mm green Cable
5 Audio Jack 3.5mm white Cable
6 Audio Jack 3.5mm red Cable
7 Audio Jack 3.5mm green Cable
9 top button
11 top button
13 top button
15 top button
16 RX TX HC-05 Bluetooth
17 RX TX HC-05 Bluetooth
18 Midi Audio jack 6.35mm white Cable
29 Audio Jack 3.5 Double Cable
21 Midi Audio jack 6.35mm green Cable
22 Audio Jack 3.5 Double Cable
26 Analog Input Auidi Hack 3.5mm White Axis X
27 Analog Input Auidi Hack 3.5mm Green Axis Y
28 Analog Input Auidi Hack 3.5mm Trigger
VBUS 5V HC-05 Bluetooth

"""
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
from check_change_pull_up_digital import CheckForChangePullUpDigital


# 🐿️ If gamepad is not found in usb_hid.devices
# Just reboot the device in boot mode and comeback.
gamepad= Gamepad(usb_hid.devices)           # Start behaving as gamepad
mouse  = Mouse(usb_hid.devices)             # Start behaving as mouse
consumer = ConsumerControl(usb_hid.devices) # Start behaving as media control
keyboard = Keyboard(usb_hid.devices)
midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1], in_channel=0, out_channel=0)


def create_pin_button(pin_number:int)->digitalio.DigitalInOut:
    pin = digitalio.DigitalInOut(pin_number)
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP
    return pin

def create_pin_analog_input(pin_number:int)->analogio.AnalogIn:
    pin = analogio.AnalogIn(pin_number)
    return pin

def set_gamepad_button(gamepad:Gamepad,text:str, button_number:int, pressed:bool):
    if text:
        print(f"Gamepad button {text} ({button_number}) set to {pressed}")
    if pressed:
        gamepad.press_buttons(button_number)
    else:
        gamepad.release_buttons(button_number)

pin02_audioJack3Cable1 = CheckForChangePullUpDigital(board.GP2)
pin03_audioJack3Cable1 = CheckForChangePullUpDigital(board.GP3)
pin04_audioJack3Cable1 = CheckForChangePullUpDigital(board.GP4)

pin05_audioJack3Cable2 = CheckForChangePullUpDigital(board.GP5)
pin06_audioJack3Cable2 = CheckForChangePullUpDigital(board.GP6)
pin07_audioJack3Cable2 = CheckForChangePullUpDigital(board.GP7)
pin09_topButton1     = CheckForChangePullUpDigital(board.GP9)
pin11_topButton2     = CheckForChangePullUpDigital(board.GP11)
pin13_topButton3     = CheckForChangePullUpDigital(board.GP13)
pin15_topButton4     = CheckForChangePullUpDigital(board.GP15)
pin18_midiJack6Cable1= CheckForChangePullUpDigital(board.GP18)
pin20_midiJack6Cable2= CheckForChangePullUpDigital(board.GP20)
pin19_audioJack2Cable1= CheckForChangePullUpDigital(board.GP19)
pin21_audioJack2Cable2= CheckForChangePullUpDigital(board.GP21)

pin26_analogAudioHack1= create_pin_analog_input(board.GP26)
pin27_analogAudioHack2= create_pin_analog_input(board.GP27)
pin28_analogAudioHack3= create_pin_analog_input(board.GP28)


def append_basic_hello(check , name:str):
    check.append_on_press_action(lambda : print(f"{name} pressed"))
    check.append_on_release_action(lambda : print(f"{name} released"))

def append_gamepad_button_action(check , name:str, button_number:int):
    check.append_on_press_action(lambda : set_gamepad_button(gamepad, name, button_number, True))
    check.append_on_release_action(lambda : set_gamepad_button(gamepad, name, button_number, False)
    )

def append_midi_note_action(check, name:str, note_number:int, velocity:int=120):
    check.append_on_press_action(lambda : midi.send(NoteOn(note_number, velocity)))
    check.append_on_release_action(lambda : midi.send(NoteOff(note_number, 0)))

append_gamepad_button_action(pin02_audioJack3Cable1, "pin02_audioJack3Cable1", 0)
append_gamepad_button_action(pin03_audioJack3Cable1, "pin03_audioJack3Cable1", 1)
append_gamepad_button_action(pin04_audioJack3Cable1, "pin04_audioJack3Cable1", 2)
append_gamepad_button_action(pin05_audioJack3Cable2, "pin05_audioJack3Cable2", 3)
append_gamepad_button_action(pin06_audioJack3Cable2, "pin06_audioJack3Cable2", 4)
append_gamepad_button_action(pin07_audioJack3Cable2, "pin07_audioJack3Cable2", 5)
append_gamepad_button_action(pin09_topButton1, "pin09_topButton1", 6)
append_gamepad_button_action(pin11_topButton2, "pin11_topButton2", 7)
append_gamepad_button_action(pin13_topButton3, "pin13_topButton3", 8)
append_gamepad_button_action(pin15_topButton4, "pin15_topButton4", 9)
append_gamepad_button_action(pin18_midiJack6Cable1, "pin18_midiJack6Cable1", 10)
append_gamepad_button_action(pin20_midiJack6Cable2, "pin20_midiJack6Cable2", 11)
append_gamepad_button_action(pin19_audioJack2Cable1, "pin19_audioJack2Cable1", 12)
append_gamepad_button_action(pin21_audioJack2Cable2, "pin21_audioJack2Cable2", 13)

append_midi_note_action(pin02_audioJack3Cable1, "pin02_audioJack3Cable1", 60)
append_midi_note_action(pin03_audioJack3Cable1, "pin03_audioJack3Cable1", 61)
append_midi_note_action(pin04_audioJack3Cable1, "pin04_audioJack3Cable1", 62)
append_midi_note_action(pin05_audioJack3Cable2, "pin05_audioJack3Cable2", 63)
append_midi_note_action(pin06_audioJack3Cable2, "pin06_audioJack3Cable2", 64)
append_midi_note_action(pin07_audioJack3Cable2, "pin07_audioJack3Cable2", 65)
append_midi_note_action(pin09_topButton1, "pin09_topButton1", 66)
append_midi_note_action(pin11_topButton2, "pin11_topButton2", 67)
append_midi_note_action(pin13_topButton3, "pin13_topButton3", 68)
append_midi_note_action(pin15_topButton4, "pin15_topButton4", 69)
append_midi_note_action(pin18_midiJack6Cable1, "pin18_midiJack6Cable1", 70)
append_midi_note_action(pin20_midiJack6Cable2, "pin20_midiJack6Cable2", 71)
append_midi_note_action(pin19_audioJack2Cable1, "pin19_audioJack2Cable1", 72)
append_midi_note_action(pin21_audioJack2Cable2, "pin21_audioJack2Cable2", 73)



analog_26_last_value = pin26_analogAudioHack1.value
analog_27_last_value = pin27_analogAudioHack2.value
analog_28_last_value = pin28_analogAudioHack3.value

while True:
    analog_26_previous_value = analog_26_last_value
    analog_27_previous_value = analog_27_last_value
    analog_28_previous_value = analog_28_last_value
    analog_26_last_value = pin26_analogAudioHack1.value
    analog_27_last_value = pin27_analogAudioHack2.value
    analog_28_last_value = pin28_analogAudioHack3.value
    pin02_audioJack3Cable1.has_changed()
    pin03_audioJack3Cable1.has_changed()
    pin04_audioJack3Cable1.has_changed()
    pin05_audioJack3Cable2.has_changed()
    pin06_audioJack3Cable2.has_changed()
    pin07_audioJack3Cable2.has_changed()
    pin09_topButton1.has_changed()
    pin11_topButton2.has_changed()
    pin13_topButton3.has_changed()
    pin15_topButton4.has_changed()
    pin18_midiJack6Cable1.has_changed()
    pin20_midiJack6Cable2.has_changed()
    pin19_audioJack2Cable1.has_changed()
    pin21_audioJack2Cable2.has_changed()
    # Print digital pin states in a readable format
    digital_states = [
        f"02:{pin02_audioJack3Cable1.get_current_value()}",
        f"03:{pin03_audioJack3Cable1.get_current_value()}",
        f"04:{pin04_audioJack3Cable1.get_current_value()}",
        f"05:{pin05_audioJack3Cable2.get_current_value()}",
        f"06:{pin06_audioJack3Cable2.get_current_value()}",
        f"07:{pin07_audioJack3Cable2.get_current_value()}",
        f"09:{pin09_topButton1.get_current_value()}",
        f"11:{pin11_topButton2.get_current_value()}",
        f"13:{pin13_topButton3.get_current_value()}",
        f"15:{pin15_topButton4.get_current_value()}",
        f"18:{pin18_midiJack6Cable1.get_current_value()}",
        f"19:{pin19_audioJack2Cable1.get_current_value()}",
        f"20:{pin20_midiJack6Cable2.get_current_value()}",
        f"21:{pin21_audioJack2Cable2.get_current_value()}"
    ]
    #print("Digital pins: " + " | ".join(digital_states))
    
    delta_26 = analog_26_last_value - analog_26_previous_value
    delta_27 = analog_27_last_value - analog_27_previous_value
    delta_28 = analog_28_last_value - analog_28_previous_value
    time.sleep(0.01)



        