import speech_recognition as sr
import os

# This hides the ALSA warnings programmatically (alternative to the terminal command)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

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

        except sr.UnknownValueError:
            continue 
        except sr.RequestError:
            print("Check internet.")
        except Exception as e:
            continue

if __name__ == "__main__":
    start_wake_word()
