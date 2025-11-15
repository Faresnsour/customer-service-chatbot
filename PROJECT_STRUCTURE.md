# Project Structure

This document explains the organization and purpose of each component in the Customer Service Chatbot API.

## Directory Structure

```
chat_bot/
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI app entry point
│   │
│   ├── api/                     # API routes and endpoints
│   │   ├── __init__.py
│   │   └── routes.py            # All API endpoints (chat, health, etc.)
│   │
│   ├── core/                    # Core configuration and utilities
│   │   ├── __init__.py
│   │   ├── config.py            # Application settings and configuration
│   │   ├── logging_config.py    # Logging setup and configuration
│   │   └── rate_limiter.py      # Rate limiting middleware
│   │
│   ├── models/                  # Data models and schemas
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic models for request/response validation
│   │
│   └── services/                # Business logic services
│       ├── __init__.py
│       ├── conversation_manager.py  # Manages conversation history and context
│       └── openai_service.py        # Handles OpenAI API interactions
│
├── static/                      # Static files (HTML, CSS, JS)
│   └── demo.html                # Demo chat interface
│
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── README.md                    # Main documentation
├── PROJECT_STRUCTURE.md         # This file
├── test_api.py                  # API testing script
├── quickstart.sh                # Quick setup script
└── run.py                       # Simple run script
```

## Component Details

### `app/main.py`
- FastAPI application initialization
- Middleware configuration (CORS, rate limiting)
- Route registration
- Lifespan events (startup/shutdown)
- Static file serving

### `app/api/routes.py`
- All API endpoints:
  - `GET /api/v1/health` - Health check
  - `POST /api/v1/chat` - Main chat endpoint
  - `GET /api/v1/conversation/{id}` - Get conversation history
  - `DELETE /api/v1/conversation/{id}` - Clear conversation

### `app/core/config.py`
- Centralized configuration management
- Environment variable loading
- Default values
- Settings validation

### `app/core/logging_config.py`
- Logging setup and configuration
- File and console handlers
- Log formatting

### `app/core/rate_limiter.py`
- Rate limiting implementation
- Request throttling
- Custom error handling

### `app/models/schemas.py`
- Pydantic models for:
  - Request validation (ChatRequest)
  - Response models (ChatResponse, HealthResponse, etc.)
  - Data structures (Message, ConversationHistory)

### `app/services/conversation_manager.py`
- Conversation history management
- Context maintenance
- Conversation timeout handling
- Message storage and retrieval

### `app/services/openai_service.py`
- OpenAI API integration
- System prompt configuration
- Error handling for API calls
- Response processing

### `static/demo.html`
- Modern, responsive chat interface
- JavaScript for API communication
- Beautiful UI with animations
- Conversation management

## Data Flow

1. **Request** → `app/api/routes.py` (endpoint handler)
2. **Validation** → `app/models/schemas.py` (Pydantic validation)
3. **Business Logic** → `app/services/` (conversation manager, OpenAI service)
4. **Response** → Back through routes to client

## Configuration Flow

1. Environment variables (`.env`) → `app/core/config.py`
2. Settings object → Used throughout application
3. Runtime configuration → Applied at startup

## Adding New Features

### Add a New Endpoint
1. Add route handler in `app/api/routes.py`
2. Add request/response models in `app/models/schemas.py`
3. Add business logic in `app/services/` if needed

### Add a New Service
1. Create new file in `app/services/`
2. Implement service class
3. Import and use in routes

### Modify Configuration
1. Add new setting in `app/core/config.py`
2. Add to `.env.example`
3. Use in application code

## Best Practices

- **Separation of Concerns**: Routes handle HTTP, services handle business logic
- **Type Safety**: Use Pydantic models for all data validation
- **Error Handling**: Centralized error handling in services
- **Logging**: Use structured logging throughout
- **Configuration**: All settings in config.py, never hardcoded
- **Testing**: Test each component independently

