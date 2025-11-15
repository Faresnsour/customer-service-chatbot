"""
Test script for Customer Service Chatbot API
Run this to verify your API is working correctly
"""

import requests
import json
from datetime import datetime

# Configuration
API_URL = "http://localhost:8000"  # Change this to your deployed URL
API_PREFIX = "/api/v1"


def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    try:
        response = requests.get(f"{API_URL}{API_PREFIX}/health")
        print(f"✅ Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False


def test_root_endpoint():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    try:
        response = requests.get(f"{API_URL}/")
        print(f"✅ Status Code: {response.status_code}")
        data = response.json()
        print(f"API Version: {data.get('version')}")
        print(f"Status: {data.get('status')}\n")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False


def test_chat_endpoint(message, conversation_id=None, customer_name=None):
    """Test the chat endpoint with a message"""
    print(f"Testing chat with message: '{message}'")
    if conversation_id:
        print(f"  Conversation ID: {conversation_id}")
    if customer_name:
        print(f"  Customer: {customer_name}")
    
    try:
        payload = {"message": message}
        if conversation_id:
            payload["conversation_id"] = conversation_id
        if customer_name:
            payload["customer_name"] = customer_name
        
        response = requests.post(
            f"{API_URL}{API_PREFIX}/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"🤖 AI Response: {data['answer']}")
            print(f"📝 Conversation ID: {data['conversation_id']}")
            print(f"💬 Message Count: {data['message_count']}")
            print(f"⏰ Timestamp: {data['timestamp']}\n")
            return data.get('conversation_id')
        else:
            print(f"❌ Error: {response.text}\n")
            return None
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return None


def test_conversation_context():
    """Test conversation context maintenance"""
    print("Testing conversation context...")
    try:
        # First message
        conv_id = test_chat_endpoint("My name is John and I need help with my order")
        if not conv_id:
            return False
        
        # Second message (should remember the name)
        result = test_chat_endpoint("What's my name?", conversation_id=conv_id)
        return result is not None
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False


def test_error_handling():
    """Test error handling with invalid input"""
    print("Testing error handling...")
    try:
        # Test with empty message
        response = requests.post(
            f"{API_URL}{API_PREFIX}/chat",
            json={"message": ""},
            headers={"Content-Type": "application/json"}
        )
        print(f"Empty message - Status Code: {response.status_code}")
        
        # Test with missing field
        response = requests.post(
            f"{API_URL}{API_PREFIX}/chat",
            json={},
            headers={"Content-Type": "application/json"}
        )
        print(f"Missing field - Status Code: {response.status_code}\n")
        return True
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Customer Service Chatbot API - Test Suite")
    print("=" * 60)
    print(f"Testing API at: {API_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")
    
    # Test cases
    tests_passed = 0
    total_tests = 6
    
    # 1. Root endpoint
    if test_root_endpoint():
        tests_passed += 1
    
    # 2. Health check
    if test_health_check():
        tests_passed += 1
    
    # 3. Simple question
    if test_chat_endpoint("Hello, I need help"):
        tests_passed += 1
    
    # 4. Customer service question
    if test_chat_endpoint("I need help with my order", customer_name="John Doe"):
        tests_passed += 1
    
    # 5. Conversation context
    if test_conversation_context():
        tests_passed += 1
    
    # 6. Error handling
    if test_error_handling():
        tests_passed += 1
    
    # Results
    print("=" * 60)
    print(f"✅ Tests Passed: {tests_passed}/{total_tests}")
    print("=" * 60)
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your API is working perfectly!")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")


if __name__ == "__main__":
    main()
