import pytest
from unittest.mock import MagicMock, patch
from src.services.audio import AudioService

@patch("src.services.audio.sr.Microphone")
@patch("src.services.audio.sr.Recognizer")
@patch("src.services.audio.pyttsx3.init")
def test_listen_success(mock_pyttsx3, mock_recognizer_class, mock_mic):
    # 1. SETUP
    mock_recognizer_instance = mock_recognizer_class.return_value
    
    # Mock the 'recognize_google' method to return text directly
    mock_recognizer_instance.recognize_google.return_value = "hello bob"
    
    # 2. EXECUTE
    audio = AudioService()
    result = audio.listen()

    # 3. VERIFY
    assert result == "hello bob"
    # Verify we actually tried to listen to the source
    mock_recognizer_instance.listen.assert_called()

@patch("src.services.audio.pyttsx3.init")
def test_speak_calls_engine(mock_pyttsx3):
    # 1. SETUP
    mock_engine = mock_pyttsx3.return_value
    
    # 2. EXECUTE
    audio = AudioService()
    audio.speak("Testing")

    # 3. VERIFY
    mock_engine.say.assert_called_with("Testing")
    mock_engine.runAndWait.assert_called_once()