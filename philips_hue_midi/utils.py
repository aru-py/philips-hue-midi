"""
utils.py

Various utilities for philips-hue-midi.
"""

from typing import Dict

from .config import Config
from .rgbxy import Converter


def save_lights_state(bridge):
    """
    Saves current light configuration (so that it can be
    restored on program exit).
    """
    state = {}
    lights = bridge.get_api()["lights"]
    for light_id in lights:
        light_state = lights[light_id]["state"]
        state[int(light_id)] = {
            k: v
            for k, v in light_state.items()
            if k in ["on", "bri", "hue", "sat", "xy"]
        }
    return state


# todo move all below
from .core.channel import Channel

hex_to_xy = Converter().hex_to_xy


def create_channels(bridge, config: Config) -> Dict[int, Channel]:
    """
    Creates channels based on lights and configuration
    """

    channels = {}
    # todo palette should be optional

    theme_xy = [hex_to_xy(color) for color in config.palette]

    # generate color pairs from theme (start, end)
    pairs = [[c1, c2] for c1 in theme_xy for c2 in theme_xy if c1 != c2]

    defaults = config.channels.pop("default", {})
    for idx, channel in config.channels.items():
        idx = int(idx)
        colors = (
            [
                hex_to_xy(color) if isinstance(color, str) else color
                for color in channel.pop("colors")
            ]
            if channel.get("colors")
            else pairs[idx]
        )
        channels[idx] = Channel(
            bridge=bridge, **{"colors": colors, **defaults, **channel}
        )
    return channels
