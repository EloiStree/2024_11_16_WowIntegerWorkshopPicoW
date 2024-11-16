"""
`Gamepad`
====================================================

* Author(s): Dan Halbert
"""

import struct
import time

from adafruit_hid import find_device


class Gamepad:
    """Emulate a generic gamepad controller with 32 buttons,
    numbered 1-32, and two joysticks, one controlling
    ``x`` and ``y`` values, and the other controlling ``z`` and
    ``r_z`` (z rotation or ``Rz``) values.

    Two additional triggers provide ``rx`` and ``ry`` values.
    The joystick values are in the range -127 to 127, and the trigger values
    are in the range 0 to 255.
    """

    def __init__(self, devices):
        """Create a Gamepad object that will send USB gamepad HID reports.

        Devices can be a list of devices that includes a gamepad device or a gamepad device
        itself. A device is any object that implements ``send_report()``, ``usage_page`` and
        ``usage``.
        """
        self._gamepad_device = find_device(devices, usage_page=0x01, usage=0x05)
        
        # Report layout:
        # report[0-3] - buttons 1-32 (32 bits)
        # report[4] - joystick 0 x: -127 to 127
        # report[5] - joystick 0 y: -127 to 127
        # report[6] - joystick 1 x: -127 to 127
        # report[7] - joystick 1 y: -127 to 127
        # report[8] - trigger rx: 0 to 255
        # report[9] - trigger ry: 0 to 255
        self._report = bytearray(10)
        self._last_report = bytearray(10)

        # Store settings separately before putting into report.
        self._buttons_state = 0
        self._joy_x = 0
        self._joy_y = 0
        self._joy_z = 0
        self._joy_r_z = 0
        self._joy_rx = 0
        self._joy_ry = 0

        # Send an initial report to test if HID device is ready.
        try:
            self.reset_all()
        except OSError:
            time.sleep(1)
            self.reset_all()

    def press_buttons(self, *buttons):
        """Press and hold the given buttons."""
        for button in buttons:
            self._buttons_state |= 1 << (self._validate_button_number(button) - 1)
        self._send()

    def release_buttons(self, *buttons):
        """Release the given buttons."""
        for button in buttons:
            self._buttons_state &= ~(1 << (self._validate_button_number(button) - 1))
        self._send()

    def release_all_buttons(self):
        """Release all the buttons."""
        self._buttons_state = 0
        self._send()

    def click_buttons(self, *buttons):
        """Press and release the given buttons."""
        self.press_buttons(*buttons)
        self.release_buttons(*buttons)

    def set_joystick_left_x_127(self, value):
        """Set the x value of the left joystick."""
        self.move_joysticks(x=value)
    def set_joystick_left_y_127(self, value):
        """Set the y value of the left joystick."""
        self.move_joysticks(y=value)
    def set_joystick_right_x_127(self, value):
        """Set the x value of the right joystick."""
        self.move_joysticks(z=value)
    def set_joystick_right_y_127(self, value):
        """Set the y value of the right joystick."""
        self.move_joysticks(r_z=value)
    def set_trigger_left_255(self, value):
        """Set the left trigger value."""
        self.move_joysticks(rx=value)
    def set_trigger_right_255(self, value):
        """Set the right trigger value."""
        self.move_joysticks(ry=value)
        
    def set_joystick_left_x_percent(self, value):
        """Set the x value of the left joystick."""
        self.set_joystick_left_x_127(int(value * 127))
    def set_joystick_left_y_percent(self, value):
        """Set the y value of the left joystick."""
        self.set_joystick_left_y_127(int(value * 127))
    def set_joystick_right_x_percent(self, value):
        """Set the x value of the right joystick."""
        self.set_joystick_right_x_127(int(value * 127))
    def set_joystick_right_y_percent(self, value):
        """Set the y value of the right joystick."""
        self.set_joystick_right_y_127(int(value * 127))
    def set_trigger_left_percent(self, value):
        """Set the left trigger value."""
        self.set_trigger_left_255(int(value * 255))
    def set_trigger_right_percent(self, value):
        """Set the right trigger value."""
        self.set_trigger_right_255(int(value * 255))
        

    def move_joysticks(self, x=None, y=None, z=None, r_z=None, rx=None, ry=None):
        """Set and send the given joystick and trigger values.
        The joysticks will remain set with the given values until changed.

        One joystick provides ``x`` and ``y`` values,
        and the other provides ``z`` and ``r_z`` (z rotation).
        Two additional triggers provide ``rx`` and ``ry`` values.

        Joystick values must be in the range -127 to 127 inclusive.
        Trigger values must be in the range 0 to 255 inclusive.

        Examples::

            # Change x and y values only.
            gp.move_joysticks(x=100, y=-50)

            # Reset all joystick and trigger values to center position.
            gp.move_joysticks(0, 0, 0, 0, 128, 128)
        """
        if x is not None:
            self._joy_x = self._validate_joystick_value(x)
        if y is not None:
            self._joy_y = self._validate_joystick_value(y)
        if z is not None:
            self._joy_z = self._validate_joystick_value(z)
        if r_z is not None:
            self._joy_r_z = self._validate_joystick_value(r_z)
        if rx is not None:
            self._joy_rx = self._validate_trigger_value(rx)
        if ry is not None:
            self._joy_ry = self._validate_trigger_value(ry)
        self._send()

    def reset_all(self):
        """Release all buttons and set joysticks and triggers to default positions."""
        self._buttons_state = 0
        self._joy_x = 0
        self._joy_y = 0
        self._joy_z = 0
        self._joy_r_z = 0
        self._joy_rx = 0
        self._joy_ry = 0
        self._send(always=True)

    def _send(self, always=False):
        """Send a report with all the existing settings.
        If ``always`` is ``False`` (the default), send only if there have been changes.
        """
        struct.pack_into(
            "<IbbbbBB",  # 'I' for 32-bit button state, followed by joystick and trigger values
            self._report,
            0,
            self._buttons_state,
            self._joy_x,
            self._joy_y,
            self._joy_z,
            self._joy_r_z,
            self._joy_rx,
            self._joy_ry,
        )

        if always or self._last_report != self._report:
            self._gamepad_device.send_report(self._report)
            self._last_report[:] = self._report

    @staticmethod
    def _validate_button_number(button):
        if not 1 <= button <= 32:
            raise ValueError("Button number must be in range 1 to 32")
        return button

    @staticmethod
    def _validate_joystick_value(value):
        if not -127 <= value <= 127:
            raise ValueError("Joystick value must be in range -127 to 127")
        return value

    @staticmethod
    def _validate_trigger_value(value):
        if not 0 <= value <= 255:
            raise ValueError("Trigger value must be in range 0 to 255")
        return value
