import struct
from collections import namedtuple
from time import sleep

import board
import digitalio
import pwmio
import usb_hid
from adafruit_debouncer import Debouncer

Panel = namedtuple("Panel", ("button", "led"))
BRIGHT = 2**16 - 1
DIM = 2**12


def create_button(pin):
    button = digitalio.DigitalInOut(pin)
    button.switch_to_input(digitalio.Pull.UP)
    return Debouncer(button, interval=0.003)


def create_led(pin):
    return pwmio.PWMOut(pin, frequency=2**16)


def update_state(state, panel, index):
    if panel.button.value is False:
        state |= 1 << index
        panel.led.duty_cycle = BRIGHT
    else:
        state &= ~(1 << index)
        panel.led.duty_cycle = DIM
    return state


def main():
    gamepad = usb_hid.devices[0]
    button_pins = (board.GP0, board.GP1, board.GP2, board.GP3)
    led_pins = (board.GP15, board.GP16, board.GP17, board.GP18)
    buttons = (create_button(pin) for pin in button_pins)
    leds = (create_led(pin) for pin in led_pins)
    panels = [Panel(button, led) for button, led in zip(buttons, leds)]
    button_state = 0x00
    while True:
        for index, panel in enumerate(panels):
            panel.button.update()
            button_state = update_state(button_state, panel, index)
        gamepad.send_report(struct.pack("<B", button_state))


main()
