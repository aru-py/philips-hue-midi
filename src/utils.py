from random import random, choice

from config import Config


def interpolate(p, color_range):
    """
    Takes in `color_range`, a pair of tuples and interpolates linearly
    at the point `p`.
    """
    x = (color_range[1][0] - color_range[0][0]) * p + color_range[0][0]
    y = (color_range[1][1] - color_range[0][1]) * p + color_range[0][1]
    return x, y


from core.channel import Channel


def save_lights_state(bridge):
    state = {}
    lights = bridge.get_api()['lights']
    for light_id in lights:
        light_state = lights[light_id]['state']
        state[int(light_id)] = {
            k: v for k, v in light_state.items()
            if k in ['on', 'bri', 'hue', 'sat', 'xy']
        }
    return state


# todo move all below


from rgbxy import Converter

converter = Converter()


def create_channels(bridge, config: Config):
    channels = {}
    # todo palette should be optional
    theme_xy = [converter.hex_to_xy(color) for color in config.palette]
    pairs = [[c1, c2] for c1 in theme_xy for c2 in theme_xy if c1 != c2]

    defaults = config.channels.pop('default')
    for idx, channel in config.channels.items():
        idx = int(idx)
        colors = [converter.hex_to_xy(color) if isinstance(color, str) else color for color in channel.pop('colors')] \
            if channel.get('colors') else pairs[idx]
        channels[idx] = Channel(bridge=bridge, **{"colors": colors, **defaults, **channel})
    return channels
