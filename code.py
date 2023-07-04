import struct
from time import sleep

import board
import digitalio
import usb_hid
from adafruit_debouncer import Debouncer


def create_button(pin):
    button = digitalio.DigitalInOut(pin)
    button.switch_to_input(digitalio.Pull.UP)
    return Debouncer(button, interval=0.003)


def update_state(state, button, index):
    if button.value is False:
        state |= 1 << index
    else:
        state &= ~(1 << index)
    return state


def main():
    gamepad = usb_hid.devices[0]
    button_pins = [board.GP0, board.GP1, board.GP2, board.GP3]
    buttons = [create_button(pin) for pin in button_pins]
    button_state = 0x00
    while True:
        for index, button in enumerate(buttons):
            button.update()
            button_state = update_state(button_state, button, index)
        gamepad.send_report(struct.pack("<B", button_state))


main()
