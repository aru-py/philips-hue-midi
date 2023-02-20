from random import random


def interpolate(p, color_range):
    """
    Takes in `color_range`, a pair of tuples and interpolates linearly
    at the point `p`.
    """
    p = (color_range[1][0] - color_range[0][0]) * (p + random() / 5) + color_range[0][0]
    y = (color_range[1][1] - color_range[0][1]) * p + color_range[0][1]
    return p, y
