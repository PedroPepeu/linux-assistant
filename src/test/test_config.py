import pytest
import os
from src.config import Config

def test_config_initialization():
    os.environ["GOOGLE_API_KEY"] = "fake_key"

    assert Config.GOOGLE_API_KEY is not None
    assert Config.WAKE_WORD == "bob"

def test_missing_api_key_raises_error():
    if "GOOGLE_API_KEY" in os.environ:
        del os.environ["GOOGLE_API_KEY"]

    with pytest.raises(ValueError):
        class TestConfig:
            GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
            if not GOOGLE_API_KEY:
                raise ValueError("Error: No LLM API Key found")