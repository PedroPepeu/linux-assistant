import speech_recognition as sr
import os

# This hides the ALSA warnings programmatically (alternative to the terminal command)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

def get_audio_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\n[Listening...]")
        # Adjust ambient noise fixed for all recognitions
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
                
                command = get_audio_input()
                print(f"Said: {command}")
                
                if "Error" not in command:
                    answer = ask_llm(command)
                    print(f"Answer: {answer}")
                    text_to_speech(answer)
                    
        except sr.UnknownValueError:
            continue 
        except sr.RequestError:
            print("Check internet.")
        except Exception as e:
            continue

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def ask_llm(prompt):
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        return "Error: No API Key found in .env file"
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"LLM Error: {e}"

import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()

    engine.setProperty('rate', 175)

    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")

if __name__ == "__main__":
    start_wake_word()
