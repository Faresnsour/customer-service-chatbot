"""
Main FastAPI application entry point
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.api.routes import router
from app.services.conversation_manager import conversation_manager

# Setup logging
logger = setup_logging()

# Try to import rate limiting (optional)
try:
    from slowapi.errors import RateLimitExceeded
    from app.core.rate_limiter import limiter, rate_limit_exceeded_handler
    RATE_LIMITING_AVAILABLE = True
except ImportError:
    logger.warning("slowapi not installed, rate limiting disabled")
    RATE_LIMITING_AVAILABLE = False
    limiter = None
    rate_limit_exceeded_handler = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("=" * 60)
    logger.info("🚀 Customer Service Chatbot API Starting...")
    logger.info("=" * 60)
    logger.info(f"Version: {settings.API_VERSION}")
    logger.info(f"OpenAI Model: {settings.OPENAI_MODEL}")
    logger.info(f"API Documentation: http://{settings.HOST}:{settings.PORT}/docs")
    logger.info("=" * 60)
    
    yield
    
    # Shutdown
    logger.info("=" * 60)
    logger.info("🛑 Customer Service Chatbot API Shutting Down...")
    logger.info("=" * 60)
    
    # Cleanup old conversations
    removed = conversation_manager.cleanup_old_conversations()
    if removed > 0:
        logger.info(f"Cleaned up {removed} expired conversations")


# Initialize FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting (if available)
if RATE_LIMITING_AVAILABLE and limiter:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
    logger.info("Rate limiting enabled")
else:
    logger.warning("Rate limiting disabled (slowapi not installed)")

# Include API routes
app.include_router(router)

# Serve static files (for demo client)
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception:
    logger.warning("Static files directory not found, skipping static file serving")


@app.get("/")
async def root():
    """
    Root endpoint - API information and quick start guide
    
    Returns:
        API information and available endpoints
    """
    return {
        "message": "🤖 Customer Service Chatbot API is running successfully!",
        "status": "active",
        "version": settings.API_VERSION,
        "description": settings.API_DESCRIPTION,
        "endpoints": {
            "health": "GET /api/v1/health - Health check",
            "chat": "POST /api/v1/chat - Send a message to the chatbot",
            "conversation": "GET /api/v1/conversation/{id} - Get conversation history",
            "documentation": "GET /docs - Interactive API documentation (Swagger UI)",
            "redoc": "GET /redoc - Alternative API documentation",
            "demo": "GET /demo - Demo chat interface"
        },
        "usage_example": {
            "method": "POST",
            "url": "/api/v1/chat",
            "body": {
                "message": "I need help with my order",
                "customer_name": "John Doe",
                "conversation_id": "optional_conversation_id"
            }
        },
        "features": [
            "Conversation context and history",
            "Personalized customer service responses",
            "Professional AI-powered assistance",
            "Easy integration with any frontend"
        ]
    }


@app.get("/demo")
async def demo():
    """Serve the demo chat interface"""
    try:
        return FileResponse("static/demo.html")
    except Exception:
        return {
            "message": "Demo interface not found",
            "instructions": "Please create a demo.html file in the static directory"
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )

