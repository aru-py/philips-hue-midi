# philips-hue-midi

## Overview

`philips-hue-midi` allows you to control your Philips Hue lights with your piano. It is inspired by the
perceptual phenomenon of Synesthesia. See it in action below:

  <img src="docs/demo.gif" width="600px">

## Getting Started

### What You'll Need

* Philips Hue Lights & Bridge
* A MIDI Keyboard

### Installation & Setup

1. **Connect your MIDI Keyboard**: Attach your MIDI keyboard to your computer and ensure it's powered on.

2. **Configuration**: Copy the `config.example.toml` as `config.toml`. Set `lights` under `channels.0` (master channel) to the list of
   Philips Hue Lights you want to control. See [full-config.example.toml](https://github.com/aru-py/philips-hue-midi/blob/main/docs/full-config.example.toml) for
   a full list of configuration options.

4. **Install Python Dependencies**: Navigate to project root and install the necessary dependencies using [pipenv](https://github.com/pypa/pipenv):
   ```
   pipenv install
   ```
5. **Run the Program**: Execute the following command:
   ```
   pipenv run python -m philips_hue_midi.main config.toml
   ```

### Technical Details

The program samples incoming MIDI events sixty times per second (defined by SAMPLE_RATE). *Controllers* are responsible for taking this list of midi events (of variable size, *M*)
and converting them to a list of midi events of size *N*, where *N* is the number of *channels*. These channels are
defined in the `config.toml` file and are collections of lights and their configurations.

Currently, the default controller is the `note_controller` which takes in *M* notes and maps to *12* channels, based on
pitch class. For example, the first channel will be activated if the note `C` is played, the second channel for `C#`,
and so forth. Therefore, your configuration should have 12 channels.

Note that channel 0 is the master channel and is used for turning lights on or off and is the default fallback channel
if the controller outputs a channel not configured. All lights you wish to control should be included in this channel.




