# gui.py

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QStatusBar
)

from PySide6.QtCore import Qt, QTimer


class SentinelWindow(QMainWindow):

    def __init__(self, devices, lock, stop_event, subnet):
        super().__init__()

        # ==========================================
        # Shared objects
        # ==========================================

        self.devices = devices
        self.lock = lock
        self.stop_event = stop_event
        self.subnet = subnet

        self.sorted_devices = []

        # ==========================================
        # Window
        # ==========================================

        self.setWindowTitle("Network Sentinel")
        self.resize(1200, 700)

        # ==========================================
        # Central Widget
        # ==========================================

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        # ==========================================
        # Title
        # ==========================================

        title = QLabel("NETWORK SENTINEL")

        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            padding:12px;
        """)

        main_layout.addWidget(title)

        # ==========================================
        # Main Layout
        # ==========================================

        body = QHBoxLayout()

        main_layout.addLayout(body)

        # ==========================================
        # LEFT PANEL
        # ==========================================

        left_frame = QFrame()

        left_frame.setFrameShape(QFrame.Shape.StyledPanel)

        left_layout = QVBoxLayout(left_frame)

        left_title = QLabel("Devices")

        left_title.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )

        left_layout.addWidget(left_title)

        self.device_list = QListWidget()
        self.device_list.setWordWrap(True)
        self.device_list.setSpacing(5)
        self.device_list.currentRowChanged.connect(
            self.show_device_details
        )

        left_layout.addWidget(self.device_list)

        body.addWidget(left_frame, 1)

        # ==========================================
        # RIGHT PANEL
        # ==========================================

        right_frame = QFrame()

        right_frame.setFrameShape(QFrame.Shape.StyledPanel)

        right_layout = QVBoxLayout(right_frame)

        right_title = QLabel("Device Details")

        right_title.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )

        right_layout.addWidget(right_title)

        self.details = QLabel(
            "Select a device from the list."
        )

        self.details.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        self.details.setWordWrap(True)

        self.details.setStyleSheet("""
            font-size:15px;
            padding:10px;
        """)

        right_layout.addWidget(self.details)

        body.addWidget(right_frame, 2)

        self.setStyleSheet("""
        QMainWindow {
            background-color: #f3f3f3;
        }

        QFrame {
            background: white;
            border: 1px solid #d0d0d0;
            border-radius: 12px;
        }

        QLabel {
            font-size: 15px;
            color: #222;
        }
        
            QListWidget::item:hover{
            background:#e7f1ff;
        }

        QListWidget {
            background: white;
            border: 1px solid #d0d0d0;
            border-radius: 16px;
            padding: 6px;
        }

        QListWidget::item {
            padding: 10px;
            border-radius: 8px;
        }

        QListWidget::item:selected {
            background: #0078D4;
            color: white;
        }

        QStatusBar {
            background: white;
        }
        """)

        # ==========================================
        # Status Bar
        # ==========================================

        self.status = QStatusBar()

        self.setStatusBar(self.status)

        self.status.showMessage(
            f"Monitoring subnet {self.subnet}"
        )

        # ==========================================
        # Auto Refresh
        # ==========================================

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.refresh_devices
        )

        self.timer.start(1000)

    # ==========================================================
    # Refresh Device List
    # ==========================================================

    def refresh_devices(self):

        current_row = self.device_list.currentRow()

        self.device_list.clear()

        with self.lock:

            self.sorted_devices = sorted(
                self.devices.values(),
                key=lambda d: d.ip
            )

            for device in self.sorted_devices:

                icon = "🟢" if device.online else "🔴"

                if device.alias:
                    name = device.alias
                elif device.hostname != "Unknown":
                    name = device.hostname
                elif device.vendor != "Unknown":
                    name = device.vendor
                else:
                    name = device.ip

                self.device_list.addItem(
                    f"{icon} {name}\n    {device.ip}"
                )

        if 0 <= current_row < len(self.sorted_devices):

            self.device_list.setCurrentRow(current_row)

    # ==========================================================
    # Show Device Details
    # ==========================================================

    def show_device_details(self, row):

        if row < 0:
            return

        if row >= len(self.sorted_devices):
            return

        device = self.sorted_devices[row]

        protocol_text = ""

        if device.protocols:

            for protocol, count in device.protocols.items():

                protocol_text += f"{protocol}: {count}\n"

        else:

            protocol_text = "No packets yet."

        text = f"""
IP Address
{device.ip}

MAC Address
{device.mac}

Hostname
{device.hostname}

Vendor
{device.vendor}

Status
{"Online" if device.online else "Offline"}

Packets
{device.packet_count}

Bytes Sent
{device.bytes_sent}

Bytes Received
{device.bytes_received}

Protocols
{protocol_text}
"""

        self.details.setText(text)