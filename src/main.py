import sys
from PyQt6.QtWidgets import QApplication
from src.gui import MainWindow
from src.workers import AssistantThread

def main():
    # 1. Setup the Qt Application
    app = QApplication(sys.argv)
    app.setApplicationName("linux-assistant") # Important for Hyprland class matching

    # 2. Setup the Window
    window = MainWindow()
    window.show()

    # 3. Setup the Worker Thread
    assistant_thread = AssistantThread()

    # 4. Connect Signals (The Wiring)
    # When the thread says "status_changed", call window.update_status
    assistant_thread.status_changed.connect(window.update_status)
    assistant_thread.user_spoke.connect(window.add_user_message)
    assistant_thread.ai_spoke.connect(window.add_ai_message)
    assistant_thread.error_occurred.connect(window.show_error)

    # 5. Start the Thread
    assistant_thread.start()

    # 6. Execute the App Loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()