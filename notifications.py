#notifications.py

from win11toast import toast


def notify_new_device(device):

    try:
        toast(
            " Network Sentinel",
            f"New device detected!\n\n"
            f"IP : {device.ip}\n"
            f"MAC: {device.mac}"
        )

    except Exception:
        pass


def notify_device_left(device):

    try:
        toast(
            "Network Sentinel",
            f"Device went offline\n\n"
            f"IP : {device.ip}\n"
            f"MAC: {device.mac}"
        )


    except Exception:
        pass

'''    
    
from win11toast import toast


def notify_new_device(device):

    try:
        toast(
            "Network Sentinel",
            f"🚨 New device detected\n\n"
            f"IP : {device.ip}\n"
            f"MAC: {device.mac}"
        )
    except Exception:
        pass


def notify_device_left(device):

    try:
        toast(
            "Network Sentinel",
            f"Device disconnected\n\n"
            f"IP : {device.ip}\n"
            f"MAC: {device.mac}"
        )
    except Exception:
        pass'''