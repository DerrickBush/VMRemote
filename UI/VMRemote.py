from tkinter import *
from threading import Timer
import time
from Util import ScreenReaderController, SettingsController, VMController, PalletsController


class VMRemote:
    tk = Tk()
    Pallets = PalletsController.Pallets()
    Settings = SettingsController.Settings()
    ScreenReader = ScreenReaderController
    VoicemeeterController = VMController.VMController()
    Pallet = None
    inputButtons = []
    outputButtons = []
    def __init__(self):
        self.Pallet = self.Pallets.getPalletDictionary()
        self.tk.geometry('18x335' + str(self.Settings.getSetting('xyposition')))
        self.tk.configure(bg = self.Pallet['windowbackground'])
        self.tk.title('Voicemeeter Remote')
        self.tk.overrideredirect(True)
        self.tk.attributes("-topmost", True)
        self.__createButtons()
        thread = Timer(1, self.__dirtyUpdate)
        thread.start()

    # Updates Pallet
    def updatePallet(self):
        self.Pallet = self.Pallets.getPalletDictionary()

    #Resizes Remote window to show slider or hide slider
    def __resize(self, input_output, channel_number):
        if not self.VoicemeeterController.isLocked:
            if(self.tk.winfo_width() == 18):
                self.tk.geometry("54x335")
                optionScale = Scale()
                scaleGainButton = Button(self.tk, text = 'Gain', fg = self.Pallet['widgettext'], bg = self.Pallet['buttonbackgroundunmuted'], activebackground = self.Pallet['buttonbackgroundunmuted'],
                                         command = lambda: self.__setScaleOption('gain', input_output, channel_number, optionScale, scaleValButton))
                scaleGainButton.bind('<Enter>', lambda eff, text="Gain Button": self.ScreenReader.outputSpeech(text))
                scaleGainButton.place(x = 20, y = 0, width = 34)

                scaleLimitButton = Button(self.tk, text="Limit", fg=self.Pallet['widgettext'], bg=self.Pallet['buttonbackgroundunmuted'], activebackground=self.Pallet['buttonbackgroundunmuted'],
                                          command=lambda: self.__setScaleOption('limit', input_output, channel_number, optionScale, scaleValButton))
                scaleLimitButton.bind("<Enter>", lambda eff, text="Limit Button": self.ScreenReader.outputSpeech(text))
                scaleLimitButton.place(x=20, y=25, width=34)

                scaleCompButton = Button(self.tk, text="Comp", fg=self.Pallet['widgettext'], bg=self.Pallet['buttonbackgroundunmuted'], activebackground=self.Pallet['buttonbackgroundunmuted'],
                                         command=lambda: self.__setScaleOption('comp', input_output, channel_number, optionScale, scaleValButton))
                scaleCompButton.bind("<Enter>", lambda eff, text="Comp Button": self.ScreenReader.outputSpeech(text))
                scaleCompButton.place(x=20, y=50, width=34)

                scaleGateButton = Button(self.tk, text="Gate", fg=self.Pallet['widgettext'], bg=self.Pallet['buttonbackgroundunmuted'],activebackground=self.Pallet['buttonbackgroundunmuted'],
                                         command=lambda: self.__setScaleOption('gate', input_output, channel_number,optionScale, scaleValButton))
                scaleGateButton.bind("<Enter>", lambda eff, text="Gate Button": self.ScreenReader.outputSpeech(text))
                scaleGateButton.place(x=20, y=75, width=34)

                scaleValButton = Button(self.tk, text=self.VoicemeeterController.getValue(input_output, channel_number, 'gain'), fg=self.Pallet['widgettext'],bg=self.Pallet['buttonbackgroundunmuted'], activebackground=self.Pallet['buttonbackgroundunmuted'],
                                        command=lambda: optionScale.set(0))
                scaleValButton.bind("<Enter>", lambda eff, text="Reset Slider Button": self.ScreenReader.outputSpeech(text))
                scaleValButton.place(x=20, y=309, width=34)

                optionScale = Scale(self.tk, bg=self.Pallet['sliderslide'], activebackground=self.Pallet['slideractive'], troughcolor=self.Pallet['sliderbackground'],
                                    highlightthickness=0, from_=self.__getRange('gain', 'up'), to=self.__getRange('gain', 'low'), showvalue=0, resolution=.1,
                                    command=lambda eff: self.VoicemeeterController.setValue(input_output, channel_number, 'gain', optionScale.get(), scaleValButton))
                optionScale.bind("<Enter>", lambda eff, text="Slider": self.ScreenReader.outputSpeech(text))
                optionScale.set(self.VoicemeeterController.getValue(input_output, channel_number, 'gain'))
                optionScale.place(x=27, y=100, h=208)
            else:
                self.tk.geometry("18x335")

    def __setScaleOption(self, option, input_output, channel_number, scale, button):
        self.ScreenReader.outputSpeech("Setting option to" + option)
        button.config(text=(self.VoicemeeterController.getValue(input_output, channel_number, option)))
        scale.set(self.VoicemeeterController.getValue(input_output, channel_number, option))
        scale.config(bg=self.Pallet['sliderslide'], activebackground=self.Pallet['slideractive'], troughcolor=self.Pallet['sliderbackground'], highlightthickness=0,
                     from_=self.__getRange(option, 'up'), to=self.__getRange(option, 'low'), showvalue=0, resolution=.1,
                     command=lambda eff: self.VoicemeeterController.setValue(input_output, channel_number, option, scale.get(), button))

    def __getRange(self, option, bound):
        if bound == 'up':
            switcher = {
                'gain': 12,
                'limit': 12,
                'comp': 10,
                'gate': 10
            }
            return switcher.get(option, "invalid input")
        elif bound == 'low':
            switcher = {
                'gain': -60,
                'limit': -40,
                'comp': 0,
                'gate': 0
            }
            return switcher.get(option, "invalid input")

    def __createButtons(self):
        ypos = 0
        self.inputButtons = []
        for input in self.VoicemeeterController.getInputs():
            button = Button(self.tk, text=self.VoicemeeterController.getName(input)[0], bg=self.VoicemeeterController.getBackgroundColor('input', input), highlightthickness=0, fg=self.Pallet['widgettext'])
            button.bind("<Button-1>",
                        lambda eff, input=input, button=button: self.VoicemeeterController.muteChannel('input', input, button, self.VoicemeeterController.getName(input)))
            button.bind("<Button-3>", lambda eff, input=input: self.__resize('input', input))
            button.bind("<Enter>", lambda eff, text=self.VoicemeeterController.getName(input): self.ScreenReader.outputSpeech(text))
            button.place(x=0, y=ypos, width=20)
            self.inputButtons.append(button)
            ypos += 25
        # Outputs
        self.outputButtons = []
        for output in self.VoicemeeterController.getOutputs():
            button = Button(self.tk, text="O" + str(output + 1), bg=self.VoicemeeterController.getBackgroundColor('output', output), highlightthickness=0, fg=self.Pallet['widgettext'])
            button.bind("<Button-1>",
                        lambda eff, output=output, button=button: self.VoicemeeterController.muteChannel('output', output, button, (str("Output " + str(output + 1)))))
            button.bind("<Button-3>", lambda eff, output=output: self.__resize('output', output))
            button.bind("<Enter>", lambda eff, text=(str("Output " + str(output + 1))): self.ScreenReader.outputSpeech(text))
            button.place(x=0, y=ypos, width=20)
            self.outputButtons.append(button)
            ypos += 25
    
        LockControl = Button(self.tk, text="", bg=self.Pallet['buttonbackgroundunmuted'], fg=self.Pallet['widgettext'])
        LockControl.place(x=0, y=325, height=10, width=20)
        LockControl.bind("<Enter>", lambda eff, text=("Lock button"): self.ScreenReader.outputSpeech(text))
        LockControl.bind("<Button-1>", lambda eff: self.Voicemeeter.lockControl(LockControl))

    def __dirtyUpdate(self):
        while True:
            if self.VoicemeeterController.getDirty():
                for input in self.VoicemeeterController.getInputs():
                    self.VoicemeeterController.updateChannel('input', input, self.inputButtons[input])
                for output in self.VoicemeeterController.getOutputs():
                    self.VoicemeeterController.updateChannel('output', output, self.outputButtons[output])
            time.sleep(0.1)

    def createWindow(self):
        self.tk.mainloop()