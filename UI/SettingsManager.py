from tkinter import *
from threading import Timer
import time
from Util import ScreenReaderController, SettingsController, VMController, PalletsController


class SettingsManager:
    tk = Tk()
    Pallets = PalletsController.Pallets()
    Settings = SettingsController.Settings()
    ScreenReader = ScreenReaderController
    VoicemeeterController = VMController.VMController()
    Pallet = None
    def __init__(self):
        self.Pallet = self.Pallets.getPalletDictionary()
        self.tk.geometry('200x400-1020+545')
        self.tk.configure(bg=self.Pallet['windowbackground'])
        self.tk.title('Settings')




    def createWindow(self):
        self.tk.mainloop()