import voicemeeter
from Util import SettingsController, PalletsController, ScreenReaderController

class VMController():
    #Import setups
    ScreenReader = ScreenReaderController
    Pallets = PalletsController.Pallets()
    Settings = SettingsController.Settings()
    #Variables
    isLocked = None
    Pallet = None
    VoicemeterRemote = None
    def __init__(self):
        self.VoicemeterRemote = voicemeeter.remote(self.Settings.getSetting('vmversion'))
        self.VoicemeterRemote.login()
        self.Pallet = self.Pallets.getPalletDictionary()
        self.isLocked = self.Settings.getSetting('lockedOnStart')

    #Updates Pallet
    def updatePallet(self):
        self.Pallet = self.Pallets.getPalletDictionary()

    #Mutes or unmutes channel, give if input or output, channel number, and the tkinter button.
    def muteChannel(self, input_output, channel_number, button, SpeechOutput):
        if input_output == 'input':
            if not self.isLocked:
                currentMute = self.VoicemeterRemote.inputs[channel_number].mute = not self.VoicemeterRemote.inputs[channel_number].mute
                if currentMute:self.ScreenReader.outputSpeech("muting" + SpeechOutput)
                else:self.ScreenReader.outputSpeech("unmuting" + SpeechOutput)
                self.VoicemeterRemote.inputs[channel_number].mute
                button.configure(bg = self.__getState(currentMute), activebackground = self.__getState(currentMute))
        elif input_output == 'output':
            if not self.isLocked:
                currentMute = self.VoicemeterRemote.outputs[channel_number].mute = not self.VoicemeterRemote.outputs[channel_number].mute
                if currentMute:self.ScreenReader.outputSpeech("muting" + SpeechOutput)
                else:self.ScreenReader.outputSpeech("unmuting" + SpeechOutput)
                self.VoicemeterRemote.outputs[channel_number].mute
                button.configure(bg=self.__getState(currentMute), activebackground=self.__getState(currentMute))

    #Updates channel
    def updateChannel(self, input_output, channel_number, button):
        if input_output == 'input':
            if not self.isLocked:
                currentMute = self.VoicemeterRemote.inputs[channel_number].mute
                button.configure(bg = self.__getState(currentMute), activebackground = self.__getState(currentMute))
        elif input_output == 'output':
            if not self.isLocked:
                currentMute = self.VoicemeterRemote.outputs[channel_number].mute
                button.configure(bg = self.__getState(currentMute), activebackground = self.__getState(currentMute))

    #Sets value of input or output for gate, limit, comp, or gain to a given value
    def setValue(self, input_output, channel_number, option, value, button):
        button.config(text = value)
        if input_output == 'input':
            if option == 'gain': self.VoicemeterRemote.inputs[channel_number].gain = value
            if option == 'limit': self.VoicemeterRemote.inputs[channel_number].limit = value
            if option == 'comp': self.VoicemeterRemote.inputs[channel_number].comp = value
            if option == 'gate': self.VoicemeterRemote.inputs[channel_number].gate = value
        elif input_output == 'output':
            if option == 'gain': self.VoicemeterRemote.outputs[channel_number].gain = value
            if option == 'limit': self.VoicemeterRemote.outputs[channel_number].limit = value
            if option == 'comp': self.VoicemeterRemote.outputs[channel_number].comp = value
            if option == 'gate': self.VoicemeterRemote.outputs[channel_number].gate = value

    #Gets current value
    def getValue(self, input_output, channel_number, option):
        if input_output == 'input':
            if option == 'gain': return round(self.VoicemeterRemote.inputs[channel_number].gain, 1)
            if option == 'limit': return round(self.VoicemeterRemote.inputs[channel_number].limit, 1)
            if option == 'comp': return round(self.VoicemeterRemote.inputs[channel_number].comp, 1)
            if option == 'gate': return round(self.VoicemeterRemote.inputs[channel_number].gate, 1)
        elif input_output == 'output':
            if option == 'gain': return round(self.VoicemeterRemote.outputs[channel_number].gain, 1)
            if option == 'limit': return round(self.VoicemeterRemote.outputs[channel_number].limit, 1)
            if option == 'comp': return round(self.VoicemeterRemote.outputs[channel_number].comp, 1)
            if option == 'gate': return round(self.VoicemeterRemote.outputs[channel_number].gate, 1)

    #Locks or unlocks input to UI
    def lockControl(self, button):
        if button.cget('bg') == self.Pallet['buttonbackgroundmuted']:
            self.isLocked = True
            button.configure(bg = self.Pallet['buttonbackgroundmuted'])
        else:
            self.isLocked = False
            button.configure(bg=self.Pallet['buttonBackgroundunmuted'])

    #Returns current background color
    def getBackgroundColor(self, input_output, channel_number):
        if input_output == 'input': return self.__getState(self.VoicemeterRemote.inputs[channel_number].mute)
        elif input_output == 'output':return self.__getState(self.VoicemeterRemote.outputs[channel_number].mute)

    #Returns if Voicemeeter values are dirty
    def getDirty(self):
        return self.VoicemeterRemote.dirty

    #Returns input name(Only works with inputs)
    def getName(self, channel_number):
        return self.VoicemeterRemote.inputs[channel_number].label

    def getInputs(self):
        inputs = self.VoicemeterRemote.inputs
        returnInputs = []
        for input in inputs:
            if input.__str__().find("PhysicalInputStrip") != -1:
                returnInputs.append(input.index)
        return returnInputs

    def getOutputs(self):
        outputs = self.VoicemeterRemote.outputs
        returnOutputs = []
        for output in outputs:
            returnOutputs.append(output.index)
        return returnOutputs

    def logout(self):
        self.VoicemeterRemote.logout()

    def __getState(self, currentMute):
        if currentMute:
            return self.Pallet['buttonbackgroundmuted']
        else:
            return self.Pallet['buttonbackgroundunmuted']
