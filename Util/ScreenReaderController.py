import accessible_output2.outputs.auto
o = accessible_output2.outputs.nvda.NVDA()

def outputSpeech(text):
    o.speak(text, interrupt=True)