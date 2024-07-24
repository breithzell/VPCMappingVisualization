import vpc
import argparse

if __name__ == "__main__":
    # Arg parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--vpcdevice', nargs=1, dest="device", choices=['VPCAlpha', 'VPCThrottleCM3', 'new'],
                        help='Name of the VPC device to map. Use "new" to create a new layout')
    parser.add_argument('--layout', nargs=1, dest='layout',
                        help='Path to the layout png file')
    parser.add_argument('--keymap', nargs=1, dest='keymap',
                        help='Path to the keymap containing the mapping used by the game')
    parser.add_argument('--game', nargs=1, dest='game', choices=['SC', 'DCS'],
                        help='Map SC or DCS type of input')
    parser.add_argument('--joyID', nargs=1, dest='joyID', default=[None],
                        help='Joystick ID you want to map. At the first execution, the tool will tell you what is available')
    parser.add_argument('--makemap', dest='makemap', default=False, action="store_true",
                        help='Ignorer all input an just start the tool to make a new map')
    
    args = parser.parse_args()

    # Main
    vpcdevice = args.device[0]
    keymap = args.keymap[0]
    layout = args.layout[0]
    game = args.game[0]
    joyID = args.joyID[0]

    # Run
    vpc.vpc(device=vpcdevice, game=game, layout=layout, keymap=keymap, joystickID=joyID)