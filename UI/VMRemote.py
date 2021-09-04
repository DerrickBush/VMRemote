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
    height = None
    scaleButtons = []
    def __init__(self):
        self.Pallet = self.Pallets.getPalletDictionary()
        self.tk.geometry('18x' + str((((len(self.VoicemeeterController.getInputs()))+len(self.VoicemeeterController.getOutputs()))*25)+10) + str(self.Settings.getSetting('xyposition')))
        self.tk.configure(bg = self.Pallet['windowbackground'])
        self.tk.title('Voicemeeter Remote')
        self.tk.overrideredirect(True)
        self.tk.attributes("-topmost", True)
        self.__createButtons()
        if (self.VoicemeeterController.getVersion() == 'basic'):
            self.height = 135
        elif (self.VoicemeeterController.getVersion() == 'banana'):
            self.height = 210
        elif (self.VoicemeeterController.getVersion() == 'potato'):
            self.height = 335
        thread = Timer(1, self.__dirtyUpdate)
        thread.start()

    # Updates Pallet
    def updatePallet(self):
        self.Pallet = self.Pallets.getPalletDictionary()

    #Resizes Remote window to show slider or hide slider
    def __resize(self, input_output, channel_number):
        print(self.tk.winfo_height())
        if not self.VoicemeeterController.isLocked:
            if(self.tk.winfo_width() == 18):
                self.tk.geometry("54x" + str(self.height))
                optionScale = Scale()
                if(self.VoicemeeterController.getVersion() == 'basic'):
                    scaleValButton = Button(self.tk,
                                            text=self.VoicemeeterController.getValue(input_output, channel_number,'gain'),
                                            fg=self.Pallet['widgettext'], bg=self.Pallet['buttonbackgroundunmuted'],
                                            activebackground=self.Pallet['buttonbackgroundunmuted'],
                                            command=lambda: optionScale.set(0))
                    scaleValButton.bind("<Enter>", lambda eff, text="Reset Slider Button": self.ScreenReader.outputSpeech(text))
                    scaleValButton.place(x=20, y=100, width=34)

                    self.__setScaleOption('gain', input_output, channel_number, optionScale, scaleValButton)
                    optionScale.place(x=27, y=0, h=100)
                elif(self.VoicemeeterController.getVersion() == 'banana'):
                    scaleValButton = Button(self.tk, text=self.VoicemeeterController.getValue(input_output, channel_number, 'gain'), fg=self.Pallet['widgettext'],bg=self.Pallet['buttonbackgroundunmuted'], activebackground=self.Pallet['buttonbackgroundunmuted'],
                                            command=lambda: optionScale.set(0))
                    scaleValButton.bind("<Enter>", lambda eff, text="Reset Slider Button": self.ScreenReader.outputSpeech(text))
                    scaleValButton.place(x=20, y=185, width=34)

                    if(input_output == "input"):
                        options = ['gain', 'limit', 'comp', 'gate']
                        self.__createScaleButtons(options, input_output, channel_number, optionScale, scaleValButton)
                        self.__setScaleOption('gain', input_output, channel_number, optionScale, scaleValButton)
                        optionScale.place(x=27, y=100, h=85)
                    else:
                        self.__setScaleOption('gain', input_output, channel_number, optionScale, scaleValButton)
                        optionScale.place(x=27, y=0, h=185)
                elif (self.VoicemeeterController.getVersion() == 'potato'):
                    scaleValButton = Button(self.tk,
                                            text=self.VoicemeeterController.getValue(input_output, channel_number,
                                                                                     'gain'),
                                            fg=self.Pallet['widgettext'], bg=self.Pallet['buttonbackgroundunmuted'],
                                            activebackground=self.Pallet['buttonbackgroundunmuted'],
                                            command=lambda: optionScale.set(0))
                    scaleValButton.bind("<Enter>",
                                        lambda eff, text="Reset Slider Button": self.ScreenReader.outputSpeech(text))
                    scaleValButton.place(x=20, y=309, width=34)

                    if (input_output == "input"):
                        options = ['gain', 'limit', 'comp', 'gate']
                        self.__createScaleButtons(options, input_output, channel_number, optionScale, scaleValButton)
                        self.__setScaleOption('gain', input_output, channel_number, optionScale, scaleValButton)
                        optionScale.place(x=27, y=100, h=208)
                    else:
                        self.__setScaleOption('gain', input_output, channel_number, optionScale, scaleValButton)
                        optionScale.place(x=27, y=0, h=308)
            else:
                self.tk.geometry("18x" + str(self.height))
                for button in self.scaleButtons:
                    button.destroy()

    def __createScaleButtons(self, options, input_output, channel_number, optionScale, scaleValButton):
        buttonY = 0
        for option in options:
            print(input_output + " " + str(channel_number) + " " + option)
            scaleButton = Button(self.tk, text=option, fg=self.Pallet['widgettext'],
                                    bg=self.Pallet['buttonbackgroundunmuted'],
                                    activebackground=self.Pallet['buttonbackgroundunmuted'])
            scaleButton.bind('<Button-1>', lambda eff, option=option, input_output=input_output, channel_number=channel_number, optionScale=optionScale, scaleValButton=scaleValButton
                                    : self.__setScaleOption(option, input_output, channel_number, optionScale,
                                                                          scaleValButton))
            scaleButton.bind('<Enter>', lambda eff, text=(option + " Button"): self.ScreenReader.outputSpeech(text))
            scaleButton.place(x=20, y=buttonY, width=34)
            buttonY += 25
            self.scaleButtons.append(scaleButton)

    def __setScaleOption(self, option, input_output, channel_number, scale, button):
        self.ScreenReader.outputSpeech("Setting option to" + option)
        button.config(text=(self.VoicemeeterController.getValue(input_output, channel_number, option)))
        scale.config(bg=self.Pallet['sliderslide'], activebackground=self.Pallet['slideractive'], troughcolor=self.Pallet['sliderbackground'], highlightthickness=0,
                     from_=self.__getRange(option, 'up'), to=self.__getRange(option, 'low'), showvalue=0, resolution=.1,
                     command = lambda eff: self.VoicemeeterController.setValue(input_output, channel_number, option, scale.get(), button))
        scale.set(self.VoicemeeterController.getValue(input_output, channel_number, option))
        # scale.bind('<Button-1>', lambda eff: self.VoicemeeterController.setValue(input_output, channel_number, option, scale.get(), button))

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
            button = Button(self.tk, text=self.VoicemeeterController.getName(input)[:2], bg=self.VoicemeeterController.getBackgroundColor('input', input), highlightthickness=0, fg=self.Pallet['widgettext'])
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
        LockControl.bind("<Button-1>", lambda eff: self.VoicemeeterController.lockControl(LockControl))

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