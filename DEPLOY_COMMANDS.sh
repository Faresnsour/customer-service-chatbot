#!/bin/bash
# Quick deploy script for GitHub

echo "🚀 GitHub Deployment Script"
echo "=========================="
echo ""

# Get repository URL
read -p "Enter your GitHub username: " USERNAME
read -p "Enter repository name (default: customer-service-chatbot): " REPO_NAME
REPO_NAME=${REPO_NAME:-customer-service-chatbot}

echo ""
echo "Repository will be: https://github.com/$USERNAME/$REPO_NAME"
read -p "Continue? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "Cancelled."
    exit 1
fi

echo ""
echo "📦 Initializing Git..."
git init

echo "📝 Adding files..."
git add .

echo "💾 Creating commit..."
git commit -m "Initial commit: Professional Customer Service Chatbot API

✨ Features:
- FastAPI backend with OpenAI integration
- Conversation memory and context management
- Rate limiting and security features
- Beautiful demo interface
- Full documentation and test suite
- Test mode support (works without API key)"

echo "🔗 Adding remote..."
git remote add origin https://github.com/$USERNAME/$REPO_NAME.git

echo "🌿 Setting branch to main..."
git branch -M main

echo ""
echo "✅ Ready to push!"
echo ""
echo "Run this command to push:"
echo "git push -u origin main"
echo ""
echo "Or enter your GitHub token when prompted."
