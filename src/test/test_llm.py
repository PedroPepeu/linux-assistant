import pytest
from unittest.mock import MagicMock, patch
from src.services.llm import GeminiService

@patch("src.services.llm.genai.Client")
def test_get_response_success(mock_client_class):
    mock_instance = mock_client_class.return_value
    mock_chat = mock_instance.chats.create.return_value

    mock_response = MagicMock()
    mock_response.text = "Hello boss"
    mock_chat.send_message.return_value = mock_response

    service = GeminiService()
    response = service.get_response("Hello")

    assert response == "Hello boss"
    mock_chat.send_message.assert_called_once_with("Hello")

@patch("src.services.llm.genai.Client")
def test_get_response_failure(mock_client_class):
    mock_instance = mock_client_class.return_value
    mock_chat = mock_instance.chats.create.return_value
    mock_chat.send_message.side_effect = Exception("API Down")

    service = GeminiService()
    response = service.get_response("Hello")

    assert "Error communication with AI" in response