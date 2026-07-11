#packet_search.py
from packet_store import get_packets


def search(text):

    text = text.lower()

    results = []

    for packet in get_packets():

        if text in str(packet).lower():
            results.append(packet)

    return results