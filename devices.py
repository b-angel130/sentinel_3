#devices.py

from datetime import datetime

from vendor import get_vendor

# Maximum number of packets kept in memory for each device
MAX_PACKET_HISTORY = 500

MAX_DPI_HISTORY = 500
class Device:

    def __init__(self, ip, mac):

        self.ip = ip
        self.mac = mac

        self.hostname = "Unknown"
        self.vendor = get_vendor(mac)

        self.alias = ""
        self.notes = ""

        self.trusted = False

        # Devices always start offline until discovered
        self.online = False

        now = datetime.now()

        self.first_seen = now
        self.last_seen = now

        self.packet_count = 0

        self.bytes_sent = 0
        self.bytes_received = 0

        self.protocols = {}

        # Packet History
        self.packet_history = []


        self.events = []
        # Sentinel 3 Deep Packet Inspection

        self.dpi_history = []

        # websites visited

        self.websites = set()

        # bandwidth samples for graphs

        self.bandwidth_history = []


    # ==========================================================
    # Status
    # ==========================================================

    def mark_seen(self):

        self.last_seen = datetime.now()
        self.online = True

    def mark_offline(self):

        self.online = False

    # ==========================================================
    # Traffic
    # ==========================================================

    def add_packet(self, protocol, size, direction):

        self.packet_count += 1

        self.protocols[protocol] = (
            self.protocols.get(protocol, 0) + 1
        )

        if direction == "sent":
            self.bytes_sent += size
        else:
            self.bytes_received += size

        self.packet_history.append({

            "time": datetime.now().isoformat(),

            "protocol": protocol,

            "size": size,

            "direction": direction

        })

        # Keep only the newest packets
        if len(self.packet_history) > MAX_PACKET_HISTORY:
            self.packet_history.pop(0)

        self.mark_seen()

    # ==========================================================
    # Database
    # ==========================================================

    def to_dict(self):

        return {

            "ip": self.ip,

            "mac": self.mac,

            "hostname": self.hostname,

            "vendor": self.vendor,

            "alias": self.alias,

            "notes": self.notes,

            "trusted": self.trusted,

            # Don't really need this, but harmless to keep
            "online": self.online,

            "first_seen": self.first_seen.isoformat(),

            "last_seen": self.last_seen.isoformat(),

            "packet_count": self.packet_count,

            "bytes_sent": self.bytes_sent,

            "bytes_received": self.bytes_received,

            "protocols": self.protocols,

            # Save only the newest 100 packets to disk
            "packet_history": self.packet_history[-100:],
            "websites": list(self.websites),
            "dpi_history": self.dpi_history[-100:],
            "bandwidth_history": self.bandwidth_history[-200:]

        }

    @classmethod
    def from_dict(cls, data):

        device = cls(
            data["ip"],
            data["mac"]
        )

        device.hostname = data.get(
            "hostname",
            "Unknown"
        )

        device.vendor = data.get(
            "vendor",
            "Unknown"
        )

        device.alias = data.get(
            "alias",
            ""
        )

        device.notes = data.get(
            "notes",
            ""
        )

        device.trusted = data.get(
            "trusted",
            False
        )

        device.online = False

        device.first_seen = datetime.fromisoformat(
            data["first_seen"]
        )

        device.last_seen = datetime.fromisoformat(
            data["last_seen"]
        )

        device.packet_count = data.get(
            "packet_count",
            0
        )

        device.bytes_sent = data.get(
            "bytes_sent",
            0
        )

        device.bytes_received = data.get(
            "bytes_received",
            0
        )

        device.protocols = data.get(
            "protocols",
            {}
        )

        device.packet_history = data.get(
            "packet_history",
            []
        )

        device.websites = set(
            data.get("websites", [])
        )

        device.dpi_history = data.get(
            "dpi_history",
            []
        )

        device.bandwidth_history = data.get(
            "bandwidth_history",
            []
        )

        return device

    # ==========================================================
    # Display
    # ==========================================================

    def __str__(self):

        name = self.alias or self.hostname

        return f"{name} ({self.ip}) | {self.mac}"


    def add_dpi_record(self, record):

        self.dpi_history.append(record)

        if len(self.dpi_history) > MAX_DPI_HISTORY:
            self.dpi_history.pop(0)

    def add_website(self, website):

        if website:
            self.websites.add(website)

    def add_bandwidth_sample(self, bytes_count):

        self.bandwidth_history.append({
            "time": datetime.now().isoformat(),
            "bytes": bytes_count
        })

        if len(self.bandwidth_history) > 300:
            self.bandwidth_history.pop(0)

    def add_dpi(self, info):

        self.dpi_history.append(info)

        if len(self.dpi_history) > 500:
            self.dpi_history.pop(0)

        if info.get("website"):
            self.websites.add(info["website"])