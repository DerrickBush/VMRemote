from Util import PalletsController
from Util import SettingsController
from Util import ScreenReaderController

from threading import Timer

from UI import VMRemote #SettingsManager

VM = VMRemote.VMRemote()
#SM = SettingsManager.SettingsManager()

VMWindow = Timer(1, VM.createWindow())
# SMWindow = Timer(1, SM.createWindow())

VMWindow.start()
# SMWindow.start()

