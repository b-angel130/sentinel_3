import threading

from scapy.all import sniff, IP, TCP, UDP, ICMP

from dpi import inspect_packet


def _get_protocol(pkt):

    if pkt.haslayer(TCP):
        return "TCP"

    elif pkt.haslayer(UDP):
        return "UDP"

    elif pkt.haslayer(ICMP):
        return "ICMP"

    return "OTHER"


def make_packet_handler(devices, lock):

    def handle_packet(pkt):

        if not pkt.haslayer(IP):
            return

        src = pkt[IP].src
        dst = pkt[IP].dst

        size = len(pkt)

        protocol = _get_protocol(pkt)

        dpi_info = inspect_packet(pkt)

        with lock:

            for device in devices.values():

                # ----------------------------
                # Packet SENT
                # ----------------------------

                if device.ip == src:

                    device.add_packet(
                        protocol,
                        size,
                        direction="sent"
                    )

                    device.add_dpi(dpi_info)

                    device.add_bandwidth_sample(size)

                # ----------------------------
                # Packet RECEIVED
                # ----------------------------

                elif device.ip == dst:

                    device.add_packet(
                        protocol,
                        size,
                        direction="received"
                    )

                    device.add_dpi(dpi_info)

                    device.add_bandwidth_sample(size)

    return handle_packet


def sniff_loop(devices, lock, stop_event, iface=None):

    handler = make_packet_handler(devices, lock)

    print("Sentinel Packet Sniffer Started...\n")

    sniff(

        prn=handler,

        store=False,

        iface=iface,

        stop_filter=lambda pkt: stop_event.is_set()

    )


def start_sniffer_thread(devices, lock, stop_event, iface=None):

    t = threading.Thread(

        target=sniff_loop,

        args=(devices, lock, stop_event, iface),

        daemon=True

    )

    t.start()

    return t