# todo move config to toml/json file
class Config:
    bridge_ip = '192.168.1.11'
    sample_rate = 240

    theme = {
        "entropy": 20,
        "transition_time_min": 10,
        "brightness_off_min": 5,
        "brightness_on_min": 60,
        "color_range": [[.3, .5], [.67, .29]]
    }

    # map channels to lights
    channel_lights_mappings = {
        0: [1, 2, 3, 4],  # master channel
        1: [1],
        2: [2, 4],
        3: [3]
    }

    # red orange hues using the CIE 1931 color space
    color_ranges = {
        1: [[.5, .1], [.19, .06]],
        2: [[.3, .5], [.67, .29]],
        3: [[.24, .32], [.19, .06]]
    }
