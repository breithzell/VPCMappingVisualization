from luaparser import ast
from luaparser import astnodes

import pprint
import textwrap
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import cv2
from devicesList import availableDevices

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

  
def extractPositionsFromKeymap(vpc):
    # driver function 
    def click_event(event, x, y, flags, params): 
        '''
        Find the position of the clicks and write them on the terminal
        '''
        # checking for left mouse clicks 
        if event == cv2.EVENT_LBUTTONDOWN: 
      
            # displaying the coordinates 
            # on the Shell 
            print(f"[{x}, {y}]")
      
            # displaying the coordinates 
            # on the image window 
            font = cv2.FONT_HERSHEY_SIMPLEX 
            cv2.putText(img, str(x) + ',' +
                        str(y), (x,y), font, 
                        1, (255, 0, 0), 2) 
            cv2.imshow('image', img)
      
        # checking for right mouse clicks      
        if event==cv2.EVENT_RBUTTONDOWN: 
      
            # displaying the coordinates 
            # on the Shell 
            print(f"[{x}, {y}]")
      
            # displaying the coordinates 
            # on the image window 
            font = cv2.FONT_HERSHEY_SIMPLEX 
            b = img[y, x, 0] 
            g = img[y, x, 1] 
            r = img[y, x, 2] 
            cv2.putText(img, str(b) + ',' +
                        str(g) + ',' + str(r), 
                        (x,y), font, 1, 
                        (255, 255, 0), 2) 
            cv2.imshow('image', img) 
    '''
    Call to get the position on a specific key map
    '''
    # reading the image 
    img = cv2.imread(vpc.img) 
  
    # displaying the image 
    cv2.imshow('image', img) 
  
    # setting mouse handler for the image 
    # and calling the click_event() function 
    cv2.setMouseCallback('image', click_event) 
  
    # wait for a key to be pressed to exit 
    cv2.waitKey(0) 
  
    # close the window 
    cv2.destroyAllWindows() 

class vpc(object):
    imgPath = str
    device = str
    keymap = str
    buttons = dict
    axis = dict
    joyID = int
        
    def createButtonList(self):
        '''
        This routine open the available joystick and provide all available buttons for future usage
        '''

        # Button position will be provided, but in the moment it's hardcoded
        if self.game == "DCS":
            # All buttons in DCS have the same name, and there is one lua file per device used. The user needs to run the too for each device individually
            joyButtonString = "JOY_BTN"
            joyAxisString = "JOY_"
        elif self.game == "SC":
            # For SC all device are present in an unique xml file. Each of these device start with "jsN" where N is an index. 
            if self.joyID is None:
                print('INFO: You did not provide a joystick ID for Star Citizen, so I assume you are mapping the Joystick ID 1')
                joyButtonString = "js1_button"
                joyAxisString = "js1_"
            else: 
                joyButtonString = f"js{self.joyID}_button"
                joyAxisString = f"js{self.joyID}_"
        else:
            print("ERROR: I do not reconize the game you're trying to map")
            exit()

        # Extract the button list based on what the config file provides
        if self.device not in availableDevices.keys():
            print('ERROR: The joystick you are trying to map does not existing in the mapping list')
            print('I am calling the mapping tool. Please click on the location of every logical button where they are supposed to be')
            print('Then update the device list (VPCMappingVisualization/devicesList.py)')
            extractPositionsFromKeymap(self)
            exit()

        # Extract the buttons available for the considered device
        for key, item in availableDevices[self.device].items():
            try:
                int(key)
            except ValueError:
                self.buttons[f'{joyAxisString}{key}'] = item
            else:
                self.buttons[ f'{joyButtonString}{key}'] = item
        
    def updateButtonList(self):
        '''
        This routine filters all the available buttons and keep only the ones relevant to the considered configuration, by parsing the mapping for the game
        It also reform the self.buttons dictionnary to allow for a pos and a text entries, for each button name
        '''
        keys, names = self.parseConfig()

        # Look for the keys that are attached to this device
        for button, name in zip(keys, names):
            try:
                tmp = self.buttons[button]
            except KeyError:
                print(f'Button {button} does not exist, skipping')
                continue
            self.buttons[button] = {}
            self.buttons[button]['pos'] = tmp
            self.buttons[button]['text'] = name
        
        # Clean unused buttons for this device
        removeKeys = []
        for key in self.buttons.keys():
            if isinstance(self.buttons[key], list):
                removeKeys.append(key)
        for key in removeKeys:
            self.buttons.pop(key)
      
    def parseConfig(self):
        if self.game == 'DCS':
            with open(self.keymap, "r+") as file:
                lines = file.readlines()
                keys = []
                names = []
                for line in lines:
                    if '\"key\"' in line:
                        keys.append(line.split('=')[-1].split('"')[1])
                    if '\"name\"' in line:
                        names.append(line.split('=')[-1].split('"')[1])

        elif self.game == 'SC':
            tree = ET.parse(self.keymap)
            root = tree.getroot()
            print(f'The available devices in the configs are:')
            for option in root.findall('options'):
                joyid, joy = option.get('instance'), option.get('Product')
                print(f'Device ID{joyid}: {joy}')
                print(f'As this code currently can only map the devices one by one, you need to make sure you are passing the correct device ID in your command call to get the correct map out')
            
            names = []
            keys = []
            for actionmap in root.findall('actionmap'):
                for action in actionmap.findall('action'):
                    names.append(action.get('name').replace('_', ' '))
                    for rebind in action.findall('rebind'):
                        keys.append(rebind.get('input'))
        else:
            print('ERROR: I do not reconize the game you are trying to load the keymaping from')
        
        return keys, names

    def autoFit(self, ax, txt=None, xy=None):
        if len(txt) == 0: return txt
        # Dirty fix from c/p
        transform = ax.transData
        ha = 'left'
        va = 'top'
        min_font_size = 6
        
        #  Different alignments give different bottom left and top right anchors.
        x, y = xy
        width = 110
        height = 40
        xa0, xa1 = {
            "center": (x - width / 2, x + width / 2),
            "left": (x, x + width),
            "right": (x - width, x),
        }[ha]
        ya0, ya1 = {
            "center": (y - height / 2, y + height / 2),
            "bottom": (y, y + height),
            "top": (y, y - height),
        }[va]
        a0 = xa0, ya0
        a1 = xa1, ya1
    
        x0, y0 = transform.transform(a0)
        x1, y1 = transform.transform(a1)
        # rectangle region size to constrain the text in pixel
        rect_width = x1 - x0
        rect_height = y1 - y0
    
        fig: Figure = ax.get_figure()
        dpi = fig.dpi
        rect_height_inch = rect_height / dpi

        # Initial fontsize according to the height of boxes
        fontsize = rect_height_inch * 72
        wrap_lines = 1
        while True:
            wrapped_txt = '\n'.join(textwrap.wrap(txt, width=len(txt)//wrap_lines))
            text: Annotation = ax.annotate(wrapped_txt, xy, ha=ha, va=va, xycoords=transform)
            text.set_fontsize(fontsize)
    
            # Adjust the fontsize according to the box size.
            bbox: Bbox = text.get_window_extent(fig.canvas.get_renderer())
            adjusted_size = fontsize * rect_width / bbox.width
            if min_font_size is None or adjusted_size >= min_font_size:
                break
            text.remove()
            wrap_lines += 1
        text.set_fontsize(adjusted_size)
        return text

    def updatePositionsAutoFit(self):
        # open image
        image = cv2.imread(self.img)
        fig, ax = plt.subplots(1, figsize=(10,10)) 
        ax.imshow(image)
        for button in self.buttons:
            pos = self.buttons[button]['pos']
            text = self.buttons[button]['text']
            self.autoFit(ax, txt=text, xy=pos)
        plt.show()
    
    def __init__(self, device, game, layout, keymap, joystickID = None):
        '''
        Initialize this routine with the paths, game, device name and let the class extract all the infos directly from that.
        '''

        self.img = layout
        self.device = device
        self.keymap = keymap
        self.joyID = joystickID
        self.game = game

        self.buttons = {}

        # Update the button list based on the args
        self.createButtonList()
        self.updateButtonList()
        # And display the figure
        self.updatePositionsAutoFit()