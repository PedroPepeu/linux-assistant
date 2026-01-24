from PyQt6.QtCore import QThread, pyqtSignal
from src.services import AudioService, GeminiService
from src.config import Config

class AssistantThread(QThread):
    user_spoke = pyqtSignal(str)
    ai_spoke = pyqtSignal(str)
    status_changed = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def run(self):
        try:
            self.status_changed.emit("Initializing services...")
            audio = AudioService()
            ai = GeminiService()

            self.status_changed.emit("Calibrating microphone...")
            audio.calibrate()

            self.status_changed.emit(f"Listening for '{Config.WAKE_WORD}'...")

            while True:
                detected_text = audio.listen(phrase_time_limit=3)

                if detected_text and Config.WAKE_WORD in detected_text:
                    self.status_changed.emit("Wake word detected!")
                    audio.speak("Yes?")

                    self.status_changed.emit("Listening for command...")
                    command = audio.listen(phrase_time_limit=10)

                    if command:
                        self.user_spoke.emit(command)
                        self.status_changed.emit("Thinking...")

                        response = ai.get_response(command)
                        self.ai_spoke.emit(response)

                        self.status_changed.emit("Speaking...")
                        audio.speak(response)
                        self.status_changed.emit(f"Ready. Listening for '{Config.WAKE_WORD}'...")
                    else:
                        self.status_changed.emit("No command detected. Resetting...")
        except Exception as e:
            self.error_occurred.emit(str(e)) 