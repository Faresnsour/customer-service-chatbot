"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class Message(BaseModel):
    """Single message in a conversation"""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[str] = Field(None, description="Message timestamp")


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Customer's message to the chatbot"
    )
    conversation_id: Optional[str] = Field(
        None,
        description="Optional conversation ID for maintaining context"
    )
    customer_name: Optional[str] = Field(
        None,
        max_length=100,
        description="Optional customer name for personalized responses"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "I need help with my order",
                "conversation_id": "conv_123",
                "customer_name": "John Doe"
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    answer: str = Field(..., description="AI-generated response to the customer")
    conversation_id: str = Field(..., description="Conversation ID for context tracking")
    timestamp: str = Field(..., description="Response timestamp in ISO format")
    message_count: int = Field(..., description="Number of messages in this conversation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "I'd be happy to help you with your order. Could you please provide your order number?",
                "conversation_id": "conv_123",
                "timestamp": "2025-01-15T14:30:00.000Z",
                "message_count": 2
            }
        }


class ConversationHistory(BaseModel):
    """Conversation history response"""
    conversation_id: str
    messages: List[Message]
    created_at: str
    last_updated: str
    message_count: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    timestamp: str = Field(..., description="Error timestamp")

