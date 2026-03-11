import queue
import sounddevice as sd
import vosk
import json
from pynput.keyboard import Controller

# tools declaration
model = vosk.Model("model")
q = queue.Queue() # to get audio pieces
keyboard = Controller()


def callback(indata, frames, time, status):
    q.put(bytes(indata))


with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
    recognizer = vosk.KaldiRecognizer(model, 16000) # config recognizer model

    print("Pode falar!")
    while True:
        data = q.get() # get queue pieces
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result()) # transform in legible content
            text = result.get("text", "")
            if text:
                print(text)
                keyboard.type(text + " ")
    