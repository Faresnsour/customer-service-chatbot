"""
API routes for the Customer Service Chatbot
"""

import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    ConversationHistory
)
from app.services.conversation_manager import conversation_manager
from app.services.openai_service import openai_service
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix=settings.API_PREFIX, tags=["chatbot"])


@router.get("/", summary="API Information")
async def api_info():
    """
    Get API information and available endpoints
    
    Returns:
        API information and endpoint list
    """
    return {
        "name": "Customer Service Chatbot API",
        "version": settings.API_VERSION,
        "status": "active",
        "endpoints": {
            "health": "GET /api/v1/health",
            "chat": "POST /api/v1/chat",
            "conversation": "GET /api/v1/conversation/{id}",
            "clear_conversation": "DELETE /api/v1/conversation/{id}"
        },
        "documentation": "/docs"
    }


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for monitoring service status
    
    Returns:
        Health status with timestamp and version
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat() + "Z",
        version=settings.API_VERSION
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, req: Request):
    """
    Main chat endpoint - processes customer messages and returns AI responses
    
    This endpoint:
    - Maintains conversation context using conversation_id
    - Provides personalized responses when customer_name is provided
    - Returns helpful customer service responses
    
    Args:
        request: ChatRequest containing the customer's message
        req: FastAPI Request object for client info
    
    Returns:
        ChatResponse with AI-generated answer, conversation_id, and metadata
    
    Raises:
        HTTPException: If the request is invalid or OpenAI API call fails
    """
    try:
        # Log incoming request
        client_host = req.client.host if req.client else "unknown"
        logger.info(
            f"Chat request from {client_host} - "
            f"Conversation: {request.conversation_id or 'new'}, "
            f"Message: {request.message[:50]}..."
        )
        
        # Get or create conversation
        conversation_id = conversation_manager.get_or_create_conversation(
            request.conversation_id
        )
        
        # Get conversation history
        conversation_history = conversation_manager.get_conversation_history_for_openai(
            conversation_id
        )
        
        # Get AI response
        ai_response = await openai_service.get_chat_response(
            user_message=request.message,
            conversation_history=conversation_history,
            customer_name=request.customer_name
        )
        
        # Add messages to conversation history
        conversation_manager.add_message(conversation_id, "user", request.message)
        conversation_manager.add_message(conversation_id, "assistant", ai_response)
        
        # Get message count
        message_count = conversation_manager.get_message_count(conversation_id)
        
        # Generate timestamp
        current_time = datetime.utcnow().isoformat() + "Z"
        
        # Log successful response
        logger.info(
            f"Response generated for conversation {conversation_id} - "
            f"Message count: {message_count}"
        )
        
        return ChatResponse(
            answer=ai_response,
            conversation_id=conversation_id,
            timestamp=current_time,
            message_count=message_count
        )
    
    except Exception as e:
        # Log error details
        error_message = str(e)
        logger.error(f"Error processing chat request: {error_message}", exc_info=True)
        
        # Provide more specific error messages
        if "quota" in error_message.lower() or "billing" in error_message.lower():
            error_detail = {
                "error": "OpenAI API Quota Exceeded",
                "message": "Your OpenAI API quota has been exceeded. Please check your billing and plan at https://platform.openai.com/account/billing",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "help": "You may need to add credits to your OpenAI account or upgrade your plan."
            }
            raise HTTPException(status_code=402, detail=error_detail)  # 402 Payment Required
        elif "invalid" in error_message.lower() or "api key" in error_message.lower():
            error_detail = {
                "error": "Invalid API Key",
                "message": "Your OpenAI API key is invalid. Please check your .env file.",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            raise HTTPException(status_code=401, detail=error_detail)  # 401 Unauthorized
        else:
            # Generic error message
            error_detail = {
                "error": "Failed to process your request",
                "message": error_message if len(error_message) < 200 else "Our customer service is temporarily unavailable. Please try again in a moment.",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            raise HTTPException(status_code=500, detail=error_detail)


@router.get("/conversation/{conversation_id}", response_model=ConversationHistory)
async def get_conversation_history(conversation_id: str):
    """
    Get conversation history for a specific conversation ID
    
    Args:
        conversation_id: The conversation ID to retrieve
        
    Returns:
        ConversationHistory with all messages
        
    Raises:
        HTTPException: If conversation not found
    """
    if conversation_id not in conversation_manager.conversations:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Conversation not found",
                "message": f"Conversation {conversation_id} does not exist or has expired"
            }
        )
    
    conv_data = conversation_manager.conversations[conversation_id]
    messages = conv_data["messages"]
    
    return ConversationHistory(
        conversation_id=conversation_id,
        messages=messages,
        created_at=conv_data["created_at"].isoformat() + "Z",
        last_updated=conv_data["last_updated"].isoformat() + "Z",
        message_count=len(messages)
    )


@router.delete("/conversation/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """
    Clear a conversation history
    
    Args:
        conversation_id: The conversation ID to clear
        
    Returns:
        Success message
    """
    if conversation_manager.clear_conversation(conversation_id):
        return {
            "message": "Conversation cleared successfully",
            "conversation_id": conversation_id
        }
    else:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Conversation not found",
                "message": f"Conversation {conversation_id} does not exist"
            }
        )

