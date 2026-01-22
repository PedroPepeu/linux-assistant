from src import Config
from src.services import GeminiService, AudioService

def main():
    print("Initializating services...")
    
    try:
        ai = GeminiService()
        audio = AudioService()

        audio.calibrate()

        print(f"Ready! Listening for : `{Config.WAKE_WORD}`")

        while True:
            detected_text = audio.listen(phrase_time_limit=3)

            if detected_text and Config.WAKE_WORD in detected_text:
                print(">>> HELLO <<<")
                audio.speak("Yes?")

                print("[Listening for command...]")
                command = audio.listen(phrase_time_limit=10)

                if command:
                    print(f"You said: {command}")

                    response = ai.get_response(command)

                    audio.speak(response)
                else:
                    print("No command detected.")

    except KeyboardInterrupt:
        print("\nStopping...")

if __name__ == "__main__":
    main()