from google import genai
from src.config import Config

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=Config.GOOGLE_API_KEY)
        self.chat = self.client.chats.create(model=Config.MODEL_NAME)

    def get_response(self, prompt):
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Error communication with AI: {e}"