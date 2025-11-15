# Customer Service Chatbot API

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A production-ready customer service chatbot API powered by OpenAI's GPT models and built with FastAPI. This solution enables businesses to deliver intelligent, context-aware automated support around the clock.

## Why This Project?

Modern customers expect instant responses. This chatbot API bridges that gap by providing intelligent, consistent support while maintaining conversation context. Whether you're running an e-commerce store, a SaaS platform, or any customer-facing business, this solution scales with your needs.

## Key Features

### Core Capabilities
- **Intelligent Conversations** - Leverages OpenAI's language models for natural, helpful responses
- **Context Retention** - Maintains conversation history for coherent multi-turn discussions
- **Async Architecture** - Built with async/await patterns for handling high concurrent loads
- **Production Hardened** - Includes rate limiting, comprehensive error handling, and security measures

### Developer Experience
- **Auto-Generated Documentation** - Swagger UI and ReDoc interfaces included
- **Type Safety** - Full Pydantic validation for all requests and responses
- **Extensive Logging** - Track conversations and debug issues effectively
- **Easy Configuration** - Environment-based settings for simple deployment
- **Demo Interface** - Test the chatbot immediately with the included web UI

### Integration Ready
- **CORS Support** - Configured for cross-origin requests
- **RESTful Design** - Standard HTTP methods and status codes
- **JSON API** - Simple request/response format
- **Stateless Operations** - Easy to scale horizontally

## Project Structure

```
chat_bot/
├── app/
│   ├── __init__.py
│   ├── main.py                      # Application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py                # API route definitions
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                # Environment configuration
│   │   ├── logging_config.py        # Structured logging setup
│   │   └── rate_limiter.py          # Rate limiting logic
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py               # Request/response models
│   └── services/
│       ├── __init__.py
│       ├── conversation_manager.py  # History management
│       └── openai_service.py        # OpenAI integration
├── static/
│   └── demo.html                    # Interactive demo UI
├── requirements.txt                 # Dependencies
├── .env.example                     # Configuration template
├── README.md                        # Documentation
└── test_api.py                      # Test suite
```

## Getting Started

### Requirements

- Python 3.10 or newer
- An OpenAI API key (sign up at [platform.openai.com](https://platform.openai.com))

### Installation Steps

1. **Get the code:**
   ```bash
   git clone <your-repo-url>
   cd chat_bot
   ```

2. **Set up your environment:**
   ```bash
   python -m venv venv
   
   # Windows:
   venv\Scripts\activate
   
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application:**
   ```bash
   cp .env.example .env
   ```
   
   Open `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

5. **Start the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Verify it's running:**
   - API documentation: http://localhost:8000/docs
   - Demo interface: http://localhost:8000/demo
   - Health check: http://localhost:8000/api/v1/health

## API Reference

### Core Endpoints

#### Get API Information
```http
GET /
```

Returns service metadata and available endpoints.

#### Health Check
```http
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T14:30:00.000Z",
  "version": "1.0.0"
}
```

#### Send Message
```http
POST /api/v1/chat
Content-Type: application/json
```

**Request:**
```json
{
  "message": "I need help with my order",
  "conversation_id": "optional_id",
  "customer_name": "Jane Smith"
}
```

**Response:**
```json
{
  "answer": "I'd be happy to help you with your order. Could you provide your order number?",
  "conversation_id": "conv_abc123",
  "timestamp": "2025-01-15T14:30:00.000Z",
  "message_count": 2
}
```

**Field Descriptions:**
- `message` (required): The customer's message
- `conversation_id` (optional): Resume an existing conversation
- `customer_name` (optional): Personalize the response
- `answer`: The chatbot's response
- `message_count`: Number of messages in this conversation

#### Retrieve Conversation
```http
GET /api/v1/conversation/{conversation_id}
```

Returns the complete message history for a conversation.

#### Clear Conversation
```http
DELETE /api/v1/conversation/{conversation_id}
```

Removes all messages from a conversation's history.

## Testing

### Quick Test with cURL
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are your business hours?"}'
```

### Python Example
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/chat",
    json={
        "message": "I have a question about billing",
        "customer_name": "Alex Johnson"
    }
)

data = response.json()
print(f"Response: {data['answer']}")
print(f"Conversation ID: {data['conversation_id']}")
```

### JavaScript/TypeScript Example
```javascript
const response = await fetch('http://localhost:8000/api/v1/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'How do I reset my password?',
    customer_name: 'Chris Lee'
  })
});

const data = await response.json();
console.log(data.answer);
```

### Run Test Suite
```bash
python test_api.py
```

## Configuration Options

All settings are managed through environment variables in your `.env` file:

### OpenAI Configuration
```env
OPENAI_API_KEY=sk-your-key-here     # Required: Your OpenAI API key
OPENAI_MODEL=gpt-3.5-turbo          # Model selection (gpt-4 for better quality)
OPENAI_TEMPERATURE=0.7               # Response creativity (0.0 = focused, 1.0 = creative)
OPENAI_MAX_TOKENS=500                # Maximum response length
```

### Server Settings
```env
API_PREFIX=/api/v1                   # API route prefix
HOST=0.0.0.0                         # Bind address
PORT=8000                            # Port number
RELOAD=true                          # Auto-reload on code changes
```

### Rate Limiting
```env
RATE_LIMIT_ENABLED=true              # Enable/disable rate limiting
RATE_LIMIT_PER_MINUTE=60             # Requests allowed per minute per IP
```

### Conversation Management
```env
MAX_CONVERSATION_HISTORY=10          # Messages to keep in context
CONVERSATION_TIMEOUT_MINUTES=30      # Inactive conversation timeout
```

### Logging
```env
LOG_LEVEL=INFO                       # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=chatbot.log                 # Log file location
```

## Deployment

### Deploy to Render

Render offers a generous free tier perfect for testing and small projects.

1. Create an account at [render.com](https://render.com)
2. Create a new Web Service and connect your GitHub repository
3. Configure the service:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables in the Render dashboard:
   - `OPENAI_API_KEY`: Your OpenAI key
   - Any other custom settings
5. Deploy and get your live URL

### Deploy to Railway

Railway provides simple, automatic deployments.

1. Sign up at [railway.app](https://railway.app)
2. Create a new project from your GitHub repository
3. Add the `OPENAI_API_KEY` environment variable
4. Railway automatically detects Python and deploys
5. Access your API at the provided URL

### Deploy to Heroku

For Heroku deployment, you'll need the Heroku CLI installed.

1. Create a `Procfile` in your project root:
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

2. Deploy:
   ```bash
   heroku create your-unique-app-name
   heroku config:set OPENAI_API_KEY=your_key_here
   git push heroku main
   ```

## Customization Guide

### Changing the AI Model

For better response quality, switch to GPT-4 (note: higher costs):

```env
OPENAI_MODEL=gpt-4
```

Or use the more affordable GPT-3.5:
```env
OPENAI_MODEL=gpt-3.5-turbo
```

### Customizing the System Prompt

The chatbot's personality and behavior are defined in `app/services/openai_service.py`. Look for the `system_prompt` variable and modify it to fit your use case:

```python
system_prompt = """You are a helpful customer service representative for [Your Company].
Be friendly, professional, and concise. Always prioritize solving the customer's issue."""
```

### Adjusting Response Length

Shorter responses (faster, cheaper):
```env
OPENAI_MAX_TOKENS=300
```

Longer, detailed responses:
```env
OPENAI_MAX_TOKENS=1000
```

### Modifying Rate Limits

For higher traffic:
```env
RATE_LIMIT_PER_MINUTE=120
```

For stricter limits:
```env
RATE_LIMIT_PER_MINUTE=30
```

## Monitoring and Logs

The application logs all conversations and errors to help you monitor performance and debug issues.

**View real-time logs:**
```bash
tail -f chatbot.log
```

**Search logs:**
```bash
grep "ERROR" chatbot.log
```

Logs include:
- Incoming requests with timestamps
- OpenAI API calls and responses
- Errors with full stack traces
- Rate limit violations
- Conversation lifecycle events

## Security Considerations

This project follows security best practices:

- **API Key Protection**: Keys are stored in environment variables, never in code
- **Rate Limiting**: Prevents abuse and controls costs
- **Input Validation**: All requests are validated with Pydantic
- **CORS Configuration**: Restrict origins in production environments
- **Error Handling**: Sensitive information is never exposed in error messages
- **Logging**: Sanitized logs without sensitive data

**Important reminders:**
- Never commit your `.env` file (already in `.gitignore`)
- Rotate API keys regularly
- Monitor OpenAI usage dashboard for unexpected spikes
- Set up billing alerts on your OpenAI account
- Use environment-specific configurations for dev/staging/prod

## Cost Management

OpenAI pricing (approximate as of 2025):
- **GPT-3.5-turbo**: ~$0.0015 per 1K tokens (input/output combined)
- **GPT-4**: ~$0.03 per 1K tokens (varies by model version)

**Cost control tips:**
- Set `OPENAI_MAX_TOKENS` appropriately
- Use GPT-3.5 for most queries, GPT-4 for complex ones
- Implement conversation timeouts
- Monitor usage at [platform.openai.com/usage](https://platform.openai.com/usage)
- Set up OpenAI usage limits in your account

## Common Use Cases

This chatbot API works well for:

- **E-commerce**: Order tracking, returns, product questions
- **SaaS Products**: Technical support, feature explanations, account help
- **Healthcare**: Appointment scheduling, basic FAQs (not medical advice)
- **Education**: Course information, enrollment help, student support
- **Real Estate**: Property inquiries, viewing schedules, basic questions
- **Hospitality**: Reservations, amenities, local recommendations
- **Financial Services**: Account queries, transaction help (not financial advice)

## Roadmap

Potential enhancements for future versions:

- **Persistent Storage**: PostgreSQL or MongoDB for conversation history
- **User Authentication**: JWT-based authentication system
- **Streaming Responses**: Server-sent events for real-time responses
- **Multi-language Support**: Automatic language detection and translation
- **Analytics Dashboard**: Conversation metrics and insights
- **Webhook Integration**: Connect to external services and CRMs
- **File Handling**: Support for image and document uploads
- **Custom Training**: Fine-tuned models for specific domains
- **A/B Testing**: Compare different prompts and models

## Troubleshooting

### Common Issues

**OpenAI API errors:**
- Check your API key is valid
- Verify you have credits in your OpenAI account
- Check OpenAI status at [status.openai.com](https://status.openai.com)

**Server won't start:**
- Ensure port 8000 isn't already in use
- Verify all dependencies are installed
- Check the `.env` file exists and is properly formatted

**Rate limit errors:**
- Adjust `RATE_LIMIT_PER_MINUTE` in your configuration
- Wait a minute and try again
- Check if multiple requests are coming from the same IP

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure nothing breaks
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

Please ensure your code follows the existing style and includes appropriate tests.

## License

This project is licensed under the MIT License. You're free to use, modify, and distribute this software for any purpose, commercial or non-commercial. See the LICENSE file for full details.

## Support

Need help? Here are your options:

- **Documentation**: Check `/docs` endpoint for API details
- **Issues**: Open an issue on GitHub for bugs or feature requests
- **Code Comments**: The codebase includes detailed comments
- **Community**: Share your implementation and learn from others

## Acknowledgments

This project builds on excellent open-source tools:

- **FastAPI** by Sebastián Ramírez - Modern Python web framework
- **OpenAI** - Cutting-edge language models
- **Uvicorn** - Lightning-fast ASGI server
- **Pydantic** - Data validation using Python type hints

Special thanks to the open-source community for making projects like this possible.

## Author

**Fares Nsour**
- GitHub: [@Faresnsour](https://github.com/Faresnsour)
- Email: z06fn8@gmail.com

## Final Notes

This chatbot API is designed to be a starting point for your customer service automation. Feel free to adapt it to your specific needs, whether that's adding custom business logic, integrating with your existing systems, or scaling to handle thousands of conversations.

The code is structured to be maintainable and extensible. Each component has a clear responsibility, making it straightforward to add new features or modify existing behavior.

If you find this project helpful, consider starring the repository and sharing it with others who might benefit from it.

---

**Built with FastAPI and OpenAI • Ready for production deployment**
