# VPC Mapping Visualization Project
This project aims to provide an easy way to visually see the in game mapping on VPC devices after the mapping has been performed in game. This is intended for all people with the memory of a goldfish that cannot remember how they mapped things. 

The method used consists on reading the configuration for a given game, and map this configuration on the available buttons / axis for a given device. Each button/axis is associated with a position from a reference key map image. When running the software, the configuration will be read, and the location for each specific button will be filled with the intented usage in your game.

I am planning to get the available buttons directly from the VPC devices to be able to deal with the convertion Logical buttons > Hardware button, but this is currently not possible. For now, the mapping does not know what button is what. You need to make sure that the device you're using has a full mapping translation dictionnary (`VPCMappingVisualization/devicesList.py`). This dictionnary must contains all the buttons you want to map, which may be more than the number of hardware buttons

## Device support
In theory it could work with any device. Only the (not implemented yet) extraction method is supposed to work only with VPC devices. 

Currently the available maps are for the devices:

### Stick (all bases)
| Device                  |
|-------------------------|
| VPC Constellation Alpha |

### Throttles
| Device                      |
|-----------------------------|
| ~~VPC MongoosT-50CM3 Throttle~~ |

The associated maps are available in `maps/`. These are from the official Virpil website. Any map will work, as long as you provide the corresponding position dictionnary (`VPCMappingVisualization/devicesList.py`).

## Game support
- Digital Combat Simulator (DCS): config needs to be exported from the game, one export per device
- Star Citizen: config available in `GamePath:\Roberts Space Industries\StarCitizen\LIVE\USER\Client\0\Controls\Mappings`


## Usage
```bash
VPCMappingVisualization.py -h
usage: VPCMappingVisualization.py [-h] [--vpcdevice {VPCAlpha}] [--layout LAYOUT] [--keymap KEYMAP] [--game {SC,DCS}]
                                  [--joyID JOYID]

options:
  -h, --help            show this help message and exit
  --vpcdevice {VPCAlpha}
                        Name of the VPC device to map
  --layout LAYOUT       Path to the layout png file
  --keymap KEYMAP       Path to the keymap containing the mapping used by the game
  --game {SC,DCS}       Map SC or DCS type of input
  --joyID JOYID         Joystick ID you want to map. At the first execution, the tool will tell you what is available
```