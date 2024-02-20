# philips-hue-midi

## Overview

Philips-hue-midi allows you to control your Philips Hue lights with your midi keyboard based on key velocity and pitch. It is inspired by the
perceptual phenomenon of Synesthesia. See it in action below:

  <img src="docs/demo.gif" width="600px">

## Getting Started

### What You'll Need

**Hardware**

Philips Hue Lights & Bridge
A MIDI Keyboard

### Prerequisites

**Hardware**

- Philips Hue Lights & Bridge
- Midi Keyboard

#### Installation & Setup

1. **Connect your MIDI Keyboard**: Attach your MIDI keyboard to your computer and ensure it's powered on.

2. **Configuration**: Copy the `config.example.toml` as `config.toml`. Set `lights` under `channels.0` to the list of
   the light id's you want to control.

3. **Install Python Dependencies**: Navigate to the root directory of the project in your terminal or command prompt and
   install the necessary dependencies using pip:
   ```
   pip install -r requirements.txt
   ```
5. **Run the Program**: Execute the following command:
   ```
   pipenv run python -m philips_hue_midi.main config.toml
   ```

### Technical Details

The program listens to MIDI events and sends MIDI events at intervals (defined by SAMPLE_RATE). By default,
this is sixty times per second. *Controllers* are responsible for taking of list of midi events (of variable size, *M*)
and converting them to a list of midi events of size *N*, where *N* is the number of *channels*. These channels are
defined in the config file and are collections of lights and their configurations.

Currently, the default controller is the `note_controller` which takes in *M* notes and maps to *12* channels, based on
pitch class. For example, the first channel will be activated if the note `C` is played, the second channel for `C#`,
and so forth. Therefore, your configuration should have 12 channels.

Note that channel 0 is the master channel and is used for turning lights on or off and is the default fallback channel
if the controller outputs a channel not configured. All lights should be included in this channel.




