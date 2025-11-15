"""
OpenAI service for handling AI chat completions
"""

import logging
from typing import List, Dict, Optional
from openai import AsyncOpenAI
from openai import APIError, RateLimitError, APIConnectionError
from app.core.config import settings

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI API"""
    
    def __init__(self):
        self.test_mode = settings.TEST_MODE
        self.api_key = settings.OPENAI_API_KEY
        
        if not self.test_mode and self.api_key:
            self.client = AsyncOpenAI(api_key=self.api_key)
        else:
            self.client = None
            if self.test_mode:
                logger.info("Running in TEST_MODE - using mock responses")
            else:
                logger.warning("No OpenAI API key found - using mock responses")
        
        self.model = settings.OPENAI_MODEL
        self.temperature = settings.OPENAI_TEMPERATURE
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        
        # Customer service system prompt
        self.system_prompt = """You are a professional, friendly, and helpful customer service representative. 
Your role is to assist customers with their inquiries, resolve issues, and provide excellent service.

Guidelines:
- Be polite, empathetic, and professional at all times
- Listen carefully to customer concerns and address them directly
- Provide clear, concise, and accurate information
- If you don't know something, admit it and offer to find the answer
- Use a warm, conversational tone while maintaining professionalism
- Ask clarifying questions when needed to better understand the customer's needs
- Offer solutions proactively when possible
- Thank customers for their patience and business

Remember: Your goal is to make every customer interaction positive and helpful."""
    
    def _get_mock_response(self, user_message: str, customer_name: Optional[str] = None) -> str:
        """Generate a mock response for testing/demo purposes"""
        greeting = f"Hello {customer_name}! " if customer_name else "Hello! "
        
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ["order", "purchase", "buy"]):
            return f"{greeting}I'd be happy to help you with your order. Could you please provide your order number so I can look it up for you?"
        elif any(word in message_lower for word in ["return", "refund", "exchange"]):
            return f"{greeting}I can assist you with returns and refunds. Please let me know your order number and the reason for the return, and I'll help you process it."
        elif any(word in message_lower for word in ["shipping", "delivery", "track"]):
            return f"{greeting}I can help you track your shipment. Please provide your tracking number or order number, and I'll check the status for you."
        elif any(word in message_lower for word in ["help", "support", "assist"]):
            return f"{greeting}I'm here to help! What can I assist you with today? I can help with orders, returns, shipping, product information, and more."
        elif any(word in message_lower for word in ["hello", "hi", "hey"]):
            return f"{greeting}Thank you for contacting us! How can I assist you today?"
        else:
            return f"{greeting}Thank you for your message. I understand you're asking about: '{user_message}'. Let me help you with that. Could you provide a bit more detail so I can assist you better?"
    
    async def get_chat_response(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        customer_name: Optional[str] = None
    ) -> str:
        """
        Get AI response from OpenAI API or mock response in test mode
        
        Args:
            user_message: The customer's message
            conversation_history: Previous messages in the conversation
            customer_name: Optional customer name for personalization
            
        Returns:
            AI-generated response string
            
        Raises:
            Exception: If OpenAI API call fails (in production mode)
        """
        # Use mock response if in test mode or no API key
        if self.test_mode or not self.client:
            logger.info("Using mock response (TEST_MODE or no API key)")
            return self._get_mock_response(user_message, customer_name)
        
        try:
            # Build messages list
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history
            messages.extend(conversation_history)
            
            # Add current user message with optional personalization
            if customer_name:
                personalized_message = f"[Customer: {customer_name}] {user_message}"
            else:
                personalized_message = user_message
            
            messages.append({"role": "user", "content": personalized_message})
            
            # Call OpenAI API
            logger.info(f"Calling OpenAI API with model: {self.model}")
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            # Extract response
            ai_response = response.choices[0].message.content.strip()
            logger.info(f"OpenAI response generated successfully (length: {len(ai_response)})")
            
            return ai_response
        
        except RateLimitError as e:
            error_msg = str(e)
            logger.error(f"OpenAI rate limit/quota error: {error_msg}")
            
            # Check if it's a quota issue
            if "quota" in error_msg.lower() or "insufficient_quota" in error_msg.lower():
                raise Exception("OpenAI API quota exceeded. Please check your billing and plan at https://platform.openai.com/account/billing")
            else:
                raise Exception("Rate limit exceeded. Please try again in a moment.")
        
        except APIConnectionError as e:
            logger.error(f"OpenAI connection error: {str(e)}")
            raise Exception("Connection error. Please check your internet connection and try again.")
        
        except APIError as e:
            error_msg = str(e)
            logger.error(f"OpenAI API error: {error_msg}")
            
            # Provide more helpful error messages
            if "quota" in error_msg.lower() or "insufficient_quota" in error_msg.lower():
                raise Exception("OpenAI API quota exceeded. Please check your billing and plan at https://platform.openai.com/account/billing")
            elif "invalid_api_key" in error_msg.lower() or "authentication" in error_msg.lower():
                raise Exception("Invalid OpenAI API key. Please check your API key in the .env file.")
            else:
                raise Exception(f"OpenAI API error: {error_msg}")
        
        except Exception as e:
            logger.error(f"Unexpected error in OpenAI service: {str(e)}", exc_info=True)
            # Re-raise the exception with a user-friendly message
            if "quota" in str(e).lower():
                raise Exception("OpenAI API quota exceeded. Please check your billing and plan.")
            raise Exception(f"An unexpected error occurred: {str(e)}")


# Global OpenAI service instance
openai_service = OpenAIService()

