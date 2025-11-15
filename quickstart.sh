#!/bin/bash

# FastAPI Chatbot API - Quick Start Script
# This script automates the setup process for the chatbot API

echo "=================================="
echo "🤖 FastAPI Chatbot API Setup"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
echo "Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is not installed.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ pip3 found${NC}"

echo ""
echo "=================================="
echo "📦 Setting up virtual environment"
echo "=================================="

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null

if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${RED}❌ Failed to activate virtual environment${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Virtual environment activated${NC}"

echo ""
echo "=================================="
echo "📥 Installing dependencies"
echo "=================================="

pip install --upgrade pip > /dev/null 2>&1
echo "Installing packages from requirements.txt..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ All dependencies installed successfully${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

echo ""
echo "=================================="
echo "🔐 Setting up environment variables"
echo "=================================="

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}⚠️  .env file created from .env.example${NC}"
    echo ""
    echo -e "${YELLOW}IMPORTANT: You need to add your OpenAI API key!${NC}"
    echo ""
    read -p "Do you want to enter your OpenAI API key now? (y/n): " answer
    
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        read -p "Enter your OpenAI API key: " api_key
        if [ ! -z "$api_key" ]; then
            # Update .env file with the API key
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                sed -i '' "s/your_openai_api_key_here/$api_key/" .env
            else
                # Linux
                sed -i "s/your_openai_api_key_here/$api_key/" .env
            fi
            echo -e "${GREEN}✅ API key saved to .env file${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Remember to edit .env and add your OpenAI API key before running the app!${NC}"
        echo "   OPENAI_API_KEY=your-actual-key-here"
    fi
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
    
    # Check if API key is set
    if grep -q "your_openai_api_key_here" .env; then
        echo -e "${YELLOW}⚠️  WARNING: Default API key detected in .env${NC}"
        echo "   Please edit .env and add your actual OpenAI API key"
    fi
fi

echo ""
echo "=================================="
echo "🎉 Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Make sure your OpenAI API key is set in .env"
echo "   ${YELLOW}OPENAI_API_KEY=your-actual-key-here${NC}"
echo ""
echo "2. Start the API server:"
echo "   ${GREEN}uvicorn app.main:app --reload${NC}"
echo "   or"
echo "   ${GREEN}python -m app.main${NC}"
echo ""
echo "3. Visit the API documentation:"
echo "   ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo "4. Access the demo interface:"
echo "   ${GREEN}http://localhost:8000/demo${NC}"
echo ""
echo "5. Run automated tests:"
echo "   ${GREEN}python test_api.py${NC}"
echo ""
echo "=================================="
echo "📚 Additional Resources"
echo "=================================="
echo ""
echo "• README.md - Complete documentation"
echo "• DEPLOYMENT.md - Deployment guides"
echo "• PROJECT_STRUCTURE.md - Project overview"
echo ""
echo "Need help? Check the documentation or visit:"
echo "https://github.com/your-username/fastapi-chatbot-api"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"