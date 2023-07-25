# Stepmania Dance Pad with Pi Pico
## CircuitPython Setup

Firmware: [CircuitPython 8.2.x](https://github.com/adafruit/circuitpython/releases/tag/8.2.0 "CircuitPython 8.2.0 Release")

- built with [Adafruit instructions](https://learn.adafruit.com/building-circuitpython/build-circuitpython)
- edit bInterval to be 0x01 (1 ms or 1000Hz) in the [usb_hid init file](https://github.com/adafruit/circuitpython/blob/main/shared-module/usb_hid/__init__.c)

board: [Adafruit KB2040](https://www.adafruit.com/product/5302 "KB2040 Product Page")

`boot.py` and `code.py` must be in the root directory of the mounted CIRCUITPY drive that appears when you connect the device


## USB descriptor

Must reside in `boot.py`

### Identification

```python
import supervisor

supervisor.set_usb_identification(
    manufacturer="Stepmania", product="Dance Pad", vid=0x7868, pid=0x7868
    )
```

Ensure `vid` and `pid` are not shared with registered usb devices if you want customize the manufacturer name and product name.

You can cross-reference a usb pid/vid database such as [this one](https://the-sz.com/products/usbid/)

### Descriptor Table

See [this excellent guide](https://eleccelerator.com/tutorial-about-usb-hid-report-descriptors/) on how to write descriptors.

The general idea is to collect data from your inputs and ensure the total amount of data is an integer number of bytes. For this stepmania pad, this will be four bits (one bit per panel). This means we have to add four dummy bits to send out a full byte of data (see lines 21-24 [in the descriptor](https://github.com/RaeedAhmed/pico-ddr/blob/main/boot.py#L21))



### Sending data

In `code.py`, `button_state` is updated as events from the panels are captured. Some bitwise operations edit the state before packing it using `struct`

See the python docs on [byte order/size/alignment](https://docs.python.org/3/library/struct.html#byte-order-size-and-alignment) and [formatting](https://docs.python.org/3/library/struct.html#format-characters) of structs. In this case, we want an unpadded, 1 byte size integer to send over usb, so we can use a little endian unsigned char (e.g "<B").

This is reflected [here](https://github.com/RaeedAhmed/pico-ddr/blob/main/code.py#L27)

```python
gamepad.send_report(struct.pack("<B", button_state))
```