# dpi.py

from scapy.all import *

from scapy.layers.http import HTTPRequest

from scapy.layers.tls.all import TLS

from scapy.layers.dns import DNS

from scapy.layers.inet import TCP, UDP, ICMP

from scapy.layers.l2 import ARP


def inspect_packet(packet):
    """
    Returns information extracted from a packet.

    Returns a dictionary so future versions can easily
    include more information.
    """

    info = {
        "protocol": "Unknown",
        "website": None,
        "summary": "",
    }

    # -----------------------------
    # ARP
    # -----------------------------

    if packet.haslayer(ARP):

        info["protocol"] = "ARP"

        info["summary"] = packet.summary()

        return info

    # -----------------------------
    # ICMP
    # -----------------------------

    if packet.haslayer(ICMP):

        info["protocol"] = "ICMP"

        info["summary"] = packet.summary()

        return info

    # -----------------------------
    # DNS
    # -----------------------------

    if packet.haslayer(DNS):

        info["protocol"] = "DNS"

        dns = packet[DNS]

        if dns.qd:

            try:

                domain = dns.qd.qname.decode()

                info["website"] = domain

                info["summary"] = f"DNS Query -> {domain}"

            except Exception:

                pass

        return info

    # -----------------------------
    # HTTP
    # -----------------------------

    if packet.haslayer(HTTPRequest):

        info["protocol"] = "HTTP"

        http = packet[HTTPRequest]

        try:

            host = http.Host.decode()

            path = http.Path.decode()

            info["website"] = host

            info["summary"] = f"HTTP GET {host}{path}"

        except Exception:

            pass

        return info

    # -----------------------------
    # TLS
    # -----------------------------

    if packet.haslayer(TLS):

        info["protocol"] = "TLS"

        info["summary"] = "Encrypted HTTPS Traffic"

        return info

    # -----------------------------
    # TCP
    # -----------------------------

    if packet.haslayer(TCP):

        info["protocol"] = "TCP"

        info["summary"] = packet.summary()

        return info

    # -----------------------------
    # UDP
    # -----------------------------

    if packet.haslayer(UDP):

        info["protocol"] = "UDP"

        info["summary"] = packet.summary()

        return info

    info["summary"] = packet.summary()

    return info