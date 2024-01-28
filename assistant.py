import json
import os
from typing import List

import pyaudio
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr

class Assistant:
    def __init__(self, wakewords: List[str]):
        self.wake_words = wakewords
        self.shutdown = False

    @staticmethod
    def speak(text: str) -> None:
        """
        Passes argument to a bash script located in the main folder.
        See speak.sh for details.
        """
        os.system(f'sh speak.sh \"{text}\"')

    @staticmethod
    def listen():
        """
        Listens for input using a VOSK model.
        See model dir for details.
        """
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=1600, input=True, frames_per_buffer=8192)
        stream.start_stream()

        while True:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening... ", end="")
                audio = r.listen(source)

                try:
                    print("Recognizing... ", end="")
                    query = r.recognize_vosk(audio, language='en-US')
                    parsed_query = json.loads(query)[
                        'text']  # Converts JSON -> dict -> plain-text; VOSK handles things weird...

                    print(f"User said: {parsed_query}")

                except Exception as e:
                    print("Exception: " + str(e))

            return parsed_query.lower()

    def listen_for_wakeword(self):
        audio_in = self.listen()
        for word in self.wake_words:
            if word in audio_in:
                print("Wake word detected!")
                ping()
                return True, audio_in
