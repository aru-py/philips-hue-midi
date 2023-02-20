import logging
import time
from typing import List, Dict

import mido
from mido import Message
from phue import Bridge

from channel import Channel
from event import Event

from logging import getLogger

from settings import Config

logger = getLogger()
logger.setLevel(logging.DEBUG)

# connect to hue lights
bridge = Bridge(Config.bridge_ip)
bridge.connect()

# set up channels
channels = {}
for channel_id, lights in Config.channel_lights_mappings.items():
    theme = Config.theme
    color_range = Config.color_ranges.get(channel_id, theme['color_range'])
    channels[channel_id] = Channel(
        bridge=bridge,
        lights=lights,
        color_range=color_range,
        brightness_off_min=theme['brightness_off_min'],
        brightness_on_min=theme['brightness_on_min'],
        entropy=theme['entropy'],
        transition_time_min=theme['transition_time_min']
    )

# turn on lights
bridge.set_light(channels[0].lights, 'on', True)

# start timer
start_time = time.time()

# event queues
queue_on: List[Event] = []
queue_off: List[Event] = []


def add_to_queue(e: Message):
    if e.type == 'control_change':
        return
    event = Event(note=e.note, velocity=e.velocity, type=e.type)
    logger.warning(event)  # log events
    if event.is_key_event():
        if event.is_on():
            queue_on.insert(0, event)
        else:
            queue_off.insert(0, event)


def event_loop(sample_rate):
    global queue_on, queue_off
    time.sleep(60 / sample_rate)

    thresholds = {
        "treble": 83, "mid": 48, "bass": 21
    }

    bass, mid, treble = [], [], []

    for event in queue_on:
        note = event.note
        if note >= thresholds['treble']:
            treble.append(event)
        elif note >= thresholds['mid']:
            mid.append(event)
        elif note >= thresholds['bass']:
            bass.append(event)

    groups: Dict[int, List[Event]] = {
        0: [],
        1: treble if len(treble) else [*mid, *bass],
        2: mid if len(mid) else [*treble, *bass],
        3: bass if len(bass) else [*mid, *treble],
    }

    for _channel_id, channel in channels.items():
        if len(groups[channel_id]) > 0:
            channel.process_event(groups[channel_id].pop(0))

    # key up events
    _queue_off = []
    for event in queue_off:
        res = channels[0].process_event(event)
        if not res:
            _queue_off.append(event)
    queue_off = _queue_off

    # clear queue
    queue_on = []


# connect to keyboard
port = mido.open_input()
port.callback = add_to_queue

while True:
    event_loop(sample_rate=Config.sample_rate)
