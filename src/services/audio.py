import speech_recognition as sr
import pyttsx3
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class AudioService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 175)

    def calibrate(self):
        with sr.Microphone() as source:
            print("[Calibrating for ambient noise...]")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("[Calibration complete.]")

    def speak(self, text):
        try:
            print(f"Assistant: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")

    def listen(self, phrase_time_limit=5):
        with sr.Microphone() as source:
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=phrase_time_limit)
                text = self.recognizer.recognize_google(audio).lower()

                return text
            except sr.WaitTimeoutError:
                return "Error: No speech detected (Timeout)"
            except sr.UnknownValueError:
                return "Error: Could not understand audio"
            except sr.RequestError:
                return "Error: Internet connection issue"   