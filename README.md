# philips-hue-midi

# Overview

Philips-hue-midi is a program that allows controlling Philips Hue lights using your midi keyboard. It is inspired by the
perceptual phenomenon of [Synesthesia](https://en.wikipedia.org/wiki/Synesthesia). See it in action below:

<p align="left">
  <img src="docs/demo.gif" width="20%">
</p>

# Getting Started

## What You'll Need

**Hardware**

Philips Hue Lights & Bridge
A MIDI Keyboard

## Prerequisites

**Hardware**

- Philips Hue Lights & Bridge
- Midi Keyboard

### Installation & Setup

1. **Connect your MIDI Keyboard**: Attach your MIDI keyboard to your computer and ensure it's powered on.

2. **Configure the Bridge IP**: Navigate to the `settings.py` file in the source directory. Replace the placeholder text
   in the `bridge_ip` field with the actual IP address of your Philips Hue bridge. You can find this by
   visiting [Philips Hue Discovery](https://discovery.meethue.com/).

3. **Setup Light Mapping**: In the same `settings.py` file, configure `channel_lights_mappings` to suit your
   preferences. The keys should be set up such that the channels correspond with the exact number of Philips Hue lights
   you wish to control.

4. **Install Python Dependencies**: Navigate to the root directory of the project in your terminal or command prompt,
   and install the necessary dependencies using pip:
   ```
   pip install -r requirements.txt
   ```
5. **Run the Program**: Execute the following command:
   ```
   python src/main.py
   ```
