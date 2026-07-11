#activity.py
from collections import deque
from datetime import datetime

MAX_EVENTS = 1000

events = deque(maxlen=MAX_EVENTS)


def log(message):
    events.append({
        "time": datetime.now(),
        "message": message
    })


def get_events():
    return list(events)


def clear():
    events.clear()