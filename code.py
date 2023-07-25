import board
import struct
import usb_hid
from keypad import Event, Keys
from pwmio import PWMOut

BRIGHT = 2**16 - 1
DIM = 2**12

gamepad = usb_hid.devices[0]
button_pins = (board.D0, board.D1, board.D2, board.D3)
led_pins = (board.D4, board.D5, board.D6, board.D7)

scanner = Keys(button_pins, value_when_pressed=False, interval=0.003)
leds = {index: PWMOut(pin, frequency=2**16) for index, pin in enumerate(led_pins)}

button = Event()
button_state = 0b0
while True:
    while scanner.events.get_into(button):
        if button.pressed:
            button_state |= 1 << button.key_number
            leds[button.key_number].duty_cycle = BRIGHT
        else:
            button_state &= ~(1 << button.key_number)
            leds[button.key_number].duty_cycle = DIM
    gamepad.send_report(struct.pack("<B", button_state))
