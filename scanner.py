# scanner.py

import threading
import time
import socket
import ipaddress
import psutil
from scapy.all import ARP, Ether, srp
from devices import Device


def get_network():
    """Detect the subnet of the interface actually used for internet traffic."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    finally:
        s.close()

    if local_ip.startswith("127."):
        return "192.168.1.0/24"  # fallback

    for interface, addresses in psutil.net_if_addrs().items():
        for addr in addresses:
            if addr.family == socket.AF_INET and addr.address == local_ip:
                network = ipaddress.IPv4Network(
                    f"{addr.address}/{addr.netmask}",
                    strict=False
                )
                return str(network)

    return "192.168.1.0/24"  # fallback


def scan_once(ip_range, devices, lock):
    print(f"Scanning {ip_range}")
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    try:
        result = srp(packet, timeout=2, verbose=0)[0]

        print(f"ARP replies: {len(result)}")

    except Exception as e:
        print(f"Scan error: {e}")
        return

    seen_macs = set()

    with lock:
        for sent, received in result:
            print(received.psrc, received.hwsrc)
            ip = received.psrc
            mac = received.hwsrc.lower()
            seen_macs.add(mac)

            if mac in devices:
                devices[mac].ip = ip
                devices[mac].mark_seen()
            else:
                new_device = Device(ip, mac)
                devices[mac] = new_device
                print(f"[NEW] Device found: {new_device}")

        for mac, device in devices.items():
            if mac not in seen_macs and device.online:
                device.mark_offline()
                print(f"[OFFLINE] {device}")


def scan_loop(ip_range, devices, lock, stop_event, interval=30):

    while not stop_event.is_set():

        try:
            scan_once(ip_range, devices, lock)

        except Exception as e:
            print("SCANNER CRASHED:", e)

        stop_event.wait(interval)


def start_scanner_thread(ip_range, devices, lock, stop_event, interval=30):
    print("Scanner thread started")
    t = threading.Thread(
        target=scan_loop,
        args=(ip_range, devices, lock, stop_event, interval),
        daemon=True
    )
    t.start()
    print("Sniffer thread started")
    return t


