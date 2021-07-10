#Imports
import sys
from os import path, makedirs
import configparser

#Initiates Pallets class
class Pallets():
    config = configparser.ConfigParser()
    _palletsDirectory = path.join(path.expanduser('~/Documents'), 'LMSoftware')
    #Initializes pallet class and checks if the file exists already, if not checks if folder exits and if so makes file, if not makes folder then file
    def __init__(self):
        if sys.platform == 'win32':
            if path.exists(path.join(self._palletsDirectory, 'pallets.ini')):
                self.config.read(path.join(self._palletsDirectory, 'pallets.ini'))
            else:
                if path.exists(self._palletsDirectory):
                    self.__createPallets()
                else:
                    makedirs(self._palletsDirectory)
                    self.__createPallets()

    #Creates default pallets file. Opens and creates new pallets.ini file then creates new config sections for light and dark theme then writes config to pallets.ini file
    def __createPallets(self):
        f = open(path.join(self._palletsDirectory, 'pallets.ini'), 'w+')
        f.close
        self.config['DEFAULT'] = {'option': 'LIGHT'}
        self.config['LIGHT'] = {'windowbackground': 'white',
                           'buttonbackgroundmuted': 'red',
                           'buttonbackgroundunmuted': 'white',
                           'sliderslide': 'white',
                           'sliderbackground': 'gray',
                           'slideractive': 'white',
                           'widgettext': 'black'}
        self.config['DARK'] = {'windowbackground': 'black',
                          'buttonbackgroundmuted': 'gray',
                          'buttonbackgroundunmuted': 'black',
                          'sliderslide': 'black',
                          'sliderbackground': 'gray',
                          'slideractive': 'black',
                          'widgettext': 'white'}
        with open(path.join(self._palletsDirectory, 'pallets.ini'), 'w') as configfile:
            self.config.write(configfile)

    #Adds pallet to pallet file. Reads in pallets.ini, creates a new section with palletName and then sets the dictionary to palletDictionary.
    #After setting palletDictionary to palletName, writes the new config file to pallets.ini
    def addPallet(self, palletName, palletDictionary):
        self.config[palletName] = palletDictionary
        with open(path.join(self._palletsDirectory, 'pallets.ini'), 'w') as configfile:
            self.config.write(configfile)

    #Removes pallet from pallet file. Reads in pallets.ini, removes palletName section then writes new config file to pallets.ini
    def removePallet(self, palletName):
        self.config.read(path.join(self._palletsDirectory, 'pallets.ini'))
        self.config.remove_section(palletName)
        with open(path.join(self._palletsDirectory, 'pallets.ini'), 'w') as configfile:
            self.config.write(configfile)
