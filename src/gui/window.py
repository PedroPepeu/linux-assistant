from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLabel
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Linux Assistant")
        self.setGeometry(100, 100, 500, 600)
        
        # Setup specific Window Class for Hyprland rules
        # You can use 'windowrulev2 = float,class:^(linux-assistant)$' in hyprland.conf
        # PyQt6 sets the class name based on the app name automatically usually,
        # but this confirms the window title.

        # Main Layout container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 1. Chat Area (Read-only)
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                font-size: 14px;
                border: none;
                padding: 10px;
            }
        """)
        layout.addWidget(self.chat_area)

        # 2. Status Bar
        self.status_label = QLabel("Initializing...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-weight: bold;
                padding: 5px;
            }
        """)
        layout.addWidget(self.status_label)

    # --- SLOTS (Functions connected to Signals) ---

    def update_status(self, text):
        self.status_label.setText(text)

    def show_error(self, text):
        self.status_label.setText(f"ERROR: {text}")
        self.status_label.setStyleSheet("color: red;")

    def add_user_message(self, text):
        self.chat_area.append(f"<div style='color: #4db6ac; text-align: right;'><b>You:</b> {text}</div>")
        self.chat_area.append("") # Spacer

    def add_ai_message(self, text):
        self.chat_area.append(f"<div style='color: #ffb74d; text-align: left;'><b>Bob:</b> {text}</div>")
        self.chat_area.append("") # Spacer