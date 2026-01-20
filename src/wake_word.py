import speech_recognition as sr
import os

# This hides the ALSA warnings programmatically (alternative to the terminal command)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

def get_audio_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\n[Listening...]")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("[Processing...]")

            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            return "Error: No speech detected (Timeout)"
        except sr.UnknownValueError:
            return "Error: Could not understand audio"
        except sr.RequestError:
            return "Error: Internet connection issue"        

def start_wake_word():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    WAKE_WORD = "bob"

    with microphone as source:
        print("Calibrating mic for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
    
    print(f"Ready! Listening for: '{WAKE_WORD}'")

    while True:
        try:
            with microphone as source:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=3)

            text = recognizer.recognize_google(audio).lower()
            print(f"Found: {text}")

            if WAKE_WORD in text:
                print(">>> HELLO <<<")
                while True:
                    command = get_audio_input()
                    print(f"Said: {command}")

        except sr.UnknownValueError:
            continue 
        except sr.RequestError:
            print("Check internet.")
        except Exception as e:
            continue

if __name__ == "__main__":
    start_wake_word()
