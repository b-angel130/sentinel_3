#packet_store.py

from collections import deque

MAX_PACKETS = 10000

packet_history = deque(maxlen=MAX_PACKETS)


def add_packet(packet):
    """
    Adds a packet dictionary to the history.
    Old packets are automatically discarded.
    """
    packet_history.append(packet)


def get_packets():
    """
    Returns all stored packets.
    """
    return list(packet_history)


def clear():
    """
    Clears packet history.
    """
    packet_history.clear()