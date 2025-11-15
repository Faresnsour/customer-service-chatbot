"""
Configuration settings for the Customer Service Chatbot API
"""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""
    
    # API Configuration
    API_TITLE: str = "Customer Service Chatbot API"
    API_DESCRIPTION: str = "Professional AI-powered customer service chatbot API"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "500"))
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = ["*"]  # In production, specify your frontend domains
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # Conversation Settings
    MAX_CONVERSATION_HISTORY: int = int(os.getenv("MAX_CONVERSATION_HISTORY", "10"))
    CONVERSATION_TIMEOUT_MINUTES: int = int(os.getenv("CONVERSATION_TIMEOUT_MINUTES", "30"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "chatbot.log")
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = os.getenv("RELOAD", "true").lower() == "true"
    
    # Test Mode (works without OpenAI API key)
    TEST_MODE: bool = os.getenv("TEST_MODE", "false").lower() == "true"


settings = Settings()

# Only validate API key if not in test mode
if not settings.OPENAI_API_KEY and not settings.TEST_MODE:
    import warnings
    warnings.warn(
        "OPENAI_API_KEY not set. Set TEST_MODE=true in .env to use demo mode, "
        "or add your OpenAI API key.",
        UserWarning
    )

