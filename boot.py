import supervisor
import usb_hid

supervisor.set_usb_identification(
    manufacturer="Stepmania", product="Dance Pad", vid=0x7868, pid=0x7868
)

gamepad_descriptor = bytes(
    (
        0x05,
        0x01,  # Usage Page (Generic Desktop Ctrls)
        0x09,
        0x05,  # Usage (Game Pad)
        0xA1,
        0x01,  # Collection (Application)
        0x85,
        0x01,  #   Report ID (1)
        0x05,
        0x09,  #   Usage Page (Button)
        0x19,
        0x01,  #   Usage Minimum (Button 1)
        0x29,
        0x04,  #   Usage Maximum (Button 4)
        0x15,
        0x00,  #   Logical Minimum (0)
        0x25,
        0x01,  #   Logical Maximum (1)
        0x75,
        0x01,  #   Report Size (1)
        0x95,
        0x04,  #   Report Count (4)  ## 4 bits
        0x81,
        0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
        0x75,
        0x01,  #   Report Size(1)
        0x95,
        0x04,  #   Report Count(4)   ## 4 bits
        0x81,
        0x03,  #   Const Value Input (Dummy)
        0xC0,  # End Collection      ## total 1 byte
    )
)


gamepad = usb_hid.Device(
    report_descriptor=gamepad_descriptor,
    usage_page=0x01,  # Generic Desktop Control       ## Must match Usage Page above!
    usage=0x05,  # Gamepad                       ## Must match Usage above!
    report_ids=(1,),  # Descriptor uses report ID 1.  ## Must match Report ID above!
    in_report_lengths=(
        1,
    ),  # This gamepad sends 1 byte in its report. ## Must match number of bytes above!
    out_report_lengths=(0,),  # It does not receive any reports.
)


usb_hid.enable((gamepad,))
