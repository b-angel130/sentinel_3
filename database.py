# database.py

import json
import os

from devices import Device


DATABASE_FOLDER = "database"

DATABASE_FILE = os.path.join(
    DATABASE_FOLDER,
    "devices.json"
)


def initialize_database():

    if not os.path.exists(DATABASE_FOLDER):

        os.makedirs(DATABASE_FOLDER)

    if not os.path.exists(DATABASE_FILE):

        with open(
                DATABASE_FILE,
                "w"
        ) as f:

            json.dump({}, f, indent=4)


def load_devices():

    initialize_database()

    try:

        with open(DATABASE_FILE, "r") as f:

            raw = json.load(f)

    except (json.JSONDecodeError, FileNotFoundError):

        raw = {}

    devices = {}

    for mac, data in raw.items():

        devices[mac] = Device.from_dict(data)

    return devices


def save_devices(devices):

    initialize_database()

    data = {}

    for mac, device in devices.items():

        data[mac] = device.to_dict()

    with open(
            DATABASE_FILE,
            "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


def save_device(device):

    devices = load_devices()

    devices[device.mac] = device

    save_devices(devices)


def delete_device(mac):

    devices = load_devices()

    if mac in devices:

        del devices[mac]

        save_devices(devices)