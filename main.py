#main.py

import sys
import threading
from database import save_devices
from PySide6.QtWidgets import QApplication

from gui import SentinelWindow
from scanner import start_scanner_thread
from sniffer import start_sniffer_thread
from database import load_devices

devices = load_devices()

lock = threading.Lock()

stop_event = threading.Event()

IP_RANGE = "192.168.1.0/24"


def main():

    app = QApplication(sys.argv)

    start_scanner_thread(
        IP_RANGE,
        devices,
        lock,
        stop_event,
        interval=10
    )

    start_sniffer_thread(
        devices,
        lock,
        stop_event
    )

    window = SentinelWindow(
        devices,
        lock,
        stop_event,
        IP_RANGE
    )

    window.show()

    exit_code = app.exec()

    stop_event.set()
    save_devices(devices)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()