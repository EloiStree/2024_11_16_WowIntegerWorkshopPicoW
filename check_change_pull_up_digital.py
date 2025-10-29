import digitalio

class CheckForChangePullUpDigital:

    def __init__(self, pin_number:int):
        pin = digitalio.DigitalInOut(pin_number)
        pin.direction = digitalio.Direction.INPUT
        pin.pull = digitalio.Pull.UP
        self.digital_input = pin
        self.last_value = pin.value
        self.on_press_action_list = []
        self.on_release_action_list = []

    def has_changed(self)->bool:
        current_value = self.digital_input.value
        has_changed = current_value != self.last_value
        self.last_value = current_value

        if has_changed:
            if current_value == False:
                for action in self.on_press_action_list:
                    action()
            else:
                for action in self.on_release_action_list:
                    action()


        return has_changed


    def get_current_value(self)->bool:
        return self.digital_input.value

    def get_previous_value(self)->bool:
        return not self.digital_input.value
    
    def append_on_press_action(self, action_function):
        self.on_press_action_list.append(action_function)
        
    def append_on_release_action(self, action_function):
        self.on_release_action_list.append(action_function)


