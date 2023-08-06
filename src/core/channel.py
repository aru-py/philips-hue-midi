import math
from random import random
from typing import Any, List, Dict
from dataclasses import dataclass

from phue import Bridge

from constants import NUM_KEYS
from event import Event
from utils import interpolate

@dataclass
class Channel:
    """
    Channel maps events to lights.
    """

    bridge: Bridge
    lights: List
    colors: List
    brightness: Dict[str, Any]
    transition: Dict[str, Any]

    # maps notes to lights todo fix event queue...?

    # todo rename
    light_states = {}
    lights_locked = set()

    async def __call__(self, event: Event):
        return self._process_keydown(event) if event.is_on() else self._process_keyup(event)

    @classmethod
    def clear_locks(cls):
        cls.lights_locked.clear()

    def _process_keydown(self, event: Event):
        for light_num in self.lights:
            if light_num in Channel.lights_locked:
                continue

            self.bridge.set_light(light_num, {
                'xy': [*interpolate(((max(40, min(event.note, 80))) - 40)/40, self.colors)],
                'bri': round(self.brightness['on_min'] + (random() * self.brightness['entropy']) - self.brightness[
                    'entropy'] / 2 + math.sqrt(event.velocity) * self.brightness['sensitivity']),
                'transitiontime': max(5, round(-event.velocity / 4 + self.transition['min'])),
            })

            Channel.light_states[light_num] = event.note
            Channel.lights_locked.add(light_num)

    def _process_keyup(self, event: Event):
        # todo optimize this algorithm

        to_remove = []
        for light_num, note in Channel.light_states.items():
            if note == event.note:
                velocity = event.velocity
                self.bridge.set_light(light_num, {
                    'bri': self.brightness['off_min'],
                    'transitiontime': max(5, round(-velocity / 4 + self.transition['min']))
                })
                to_remove.append(light_num)

        for light_num in to_remove:
            Channel.light_states.pop(light_num)
