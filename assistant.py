import json
import os
from typing import List
from pydub.generators import Sine
from pydub.playback import play
import pyaudio
import speech_recognition as sr


def ping():
    """
    A somewhat annoying multipurpose chirp sound. Might get rid of this...
    """
    frequency = 850.5  # Hz
    duration = 100  # ms

    sine_wave = Sine(frequency)
    tone = sine_wave.to_audio_segment(duration=duration)
    play(tone)
    play(tone)


class Assistant:
    def __init__(self, wakewords: List[str]):
        self.wake_words = wakewords
        self.shutdown = False

    # I/O, spoken word processing, and TTS
    @staticmethod
    def speak(text: str) -> None:
        """
        Passes argument to a bash script located in the main folder. Currently using a piper-tts model for this.
        See speak.sh for details.
        """
        os.system(f'sh speak.sh \"{text}\"')

    @staticmethod
    def listen():
        """
        Listens for input using a VOSK model, then returns plain-text user input.
        """
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=1600, input=True, frames_per_buffer=8192)
        stream.start_stream()

        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening... ", end="")
            audio = r.listen(source)

            try:
                print("Recognizing... ")
                query = r.recognize_vosk(audio, language='en-US')
                parsed_query = json.loads(query)[
                    'text']  # Converts JSON -> dict -> plain-text; VOSK handles things weird...

                print(f"User said: {parsed_query}")

            except Exception as e:
                print("Exception: " + str(e))

        return parsed_query.lower()

    def listen_for_wakeword(self):
        """
        Self-explanatory: listens and identifies if a wakeword is present in the text. If it is, the whole command
        gets passed back out.
        """
        input_string = self.listen()
        for word in self.wake_words:
            if word in input_string:
                print("Wake word detected!")
                return True, input_string

    # Command execution, parsing, and logics
    def process_command(self, command):
        """
        A bit hacky for now, but this essentially serves as a buffer between the intent recognizer and the
        skill executor.
        """
        print("Processing... ", end="")
        intended_skills = self.find_intents(command)
        for skill in intended_skills:
            reply = self.execute_skill(skill)
            self.speak(reply)

    def find_intents(self, command):
        """
        Parses through a dict to determine which keywords were uttered in the user command; returns list of
        intended commands to be executed.
        """
        print("Determining intents... ", end="")
        intents = {
            ("hello", "how are you", "what's up"): "chit_chat",
            ("who are you", "what do you do"): "introductions",
        }

        found_intents = [intent_name for keywords, intent_name in intents.items() if
                         any(keyword in command for keyword in keywords)]

        print(f"Intents: {found_intents}")
        return found_intents

    def execute_skill(self, skill):
        # TODO: Create skill object, figure out logics involved (importing list of skills and associated keywords,
        #  executing skills, etc.) Current system is a little too "hacky"
        # TODO: Create some basic skills:
        #   - Wikipedia
        #   - Time and date
        #   - Alarm
        #   - DJ
        #   - Therapy mode
        print(f"Executing skill: {skill}")
        if skill == 'chit_chat':
            return 'Hello! I am well. How can I help you today?'
        if skill == 'introductions':
            return 'I am Carolyn, I am a text-to-speech virtual assistant designed to assit my users.'
        else:
            return 'I\'m sorry, I didn\'t catch that. Could you repeat it?'
