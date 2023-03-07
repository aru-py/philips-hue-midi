# philips-hue-midi


## Overview

The project allows you to control your Philips Hue lights using your piano or midi keyboard. It was inspired by the perceptual phenomenon of [Synesthesia](https://en.wikipedia.org/wiki/Synesthesia).

<p align="left">
  <img src="docs/demo.gif" alt="Scriabin Demo" width="50%">
</p>

## Usage

### Prerequisites
* Midi Keyboard
* Philips Hue Lights

### Running It

1. Connect your keyboard to your computer with a midi cable and make sure that your Hue Bridge is on the same network as your computer. 

2. Configure `settings.py` such that `bridge_ip` points to the ip address of your Philips Hue bridge (using https://discovery.meethue.com/). Configure the keys of `channel_lights_mappings` so that the channels map to the right number of Hue Lights that you want to use. Change other settings if wanted.

3. Install requirements and run ``python src/main.py``


## Notes

The program runs a loop every `60/sample rate` seconds, checking for new input notes. Based on the notes in the interval, the program determines the light configuration. 

Currently, the mapping is fairly straightforward, flashing all the lights on single notes (color determined by pitch) or flashing different lights if multiple notes are played in an interval (color determined by bass/mid/treble). In the future, it would be interesting to map colors based on the "emotion" of a piece based on something like [this](https://en.wikipedia.org/wiki/Alexander_Scriabin#/media/File:Scriabin-Circle.svg). 

