#Imports
import sys
from os import path, makedirs
import configparser
import ast

#Initialize Settings class
class Settings():
    # Initiates config parser as well as checks if OS is supported and if it is sets proper directory location for user files.
    config = configparser.ConfigParser()
    if sys.platform == 'win32':
        _settingsDirectory = path.join(path.expanduser('~/Documents'), 'LMSoftware/VMRemote')
    else:
        print("This system is not supported")
        exit()

    #Initializes Settings class and checks if settings.ini exists in the settings directory, if not it will make the file and directory if needed.
    def __init__(self):
        if sys.platform == 'win32':
            if path.exists(path.join(self._settingsDirectory, 'settings.ini')):
                self.config.read(path.join(self._settingsDirectory, 'settings.ini'))
            else:
                if path.exists(self._settingsDirectory):
                    self.__createSettings()
                else:
                    makedirs(self._settingsDirectory)
                    self.__createSettings()

    # Creates default settings and writes it to settings.ini
    def __createSettings(self):
        f = open(path.join(self._settingsDirectory, 'settings.ini'), 'w+')
        f.close
        self.config['SETTINGS'] = {'version': '0.1',
                                   'XYPosition': 'None',
                                   'ScreenReader': 'None',
                                   'VMVersion': 'None',
                                   'ignoredInputs': "None",
                                   'ignoredOutputs': "None",
                                   'lockedOnStart': 'False'}
        with open(path.join(self._settingsDirectory, 'settings.ini'), 'w') as configfile:
            self.config.write(configfile)

    #Gets a setting value
    def getSetting(self, setting):
        return ast.literal_eval(self.config['SETTINGS'][setting])

    #Sets a setting value to a new value
    def setSetting(self, setting, newValue):
        self.config['SETTINGS'][setting] = newValue
        with open(path.join(self._settingsDirectory, 'settings.ini'), 'w') as configfile:
            self.config.write(configfile)