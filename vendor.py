# vendor.py

OUI_DATABASE = {
    "78:24:AF": "Intel",
    "EC:08:6B": "TP-Link",
    "FA:23:29": "Unknown (Randomized MAC)",
}


def get_vendor(mac):

    prefix = mac.upper()[0:8]

    return OUI_DATABASE.get(prefix, "Unknown")