"""
Conversation management service for maintaining chat history and context
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from app.models.schemas import Message
from app.core.config import settings


class ConversationManager:
    """Manages conversation history and context"""
    
    def __init__(self):
        self.conversations: Dict[str, Dict] = {}
        self.timeout_minutes = settings.CONVERSATION_TIMEOUT_MINUTES
        self.max_history = settings.MAX_CONVERSATION_HISTORY
    
    def get_or_create_conversation(self, conversation_id: Optional[str] = None) -> str:
        """
        Get existing conversation ID or create a new one
        
        Args:
            conversation_id: Optional existing conversation ID
            
        Returns:
            Conversation ID string
        """
        if conversation_id and conversation_id in self.conversations:
            # Check if conversation has timed out
            last_updated = self.conversations[conversation_id]["last_updated"]
            if datetime.now() - last_updated > timedelta(minutes=self.timeout_minutes):
                # Conversation timed out, create new one
                del self.conversations[conversation_id]
                conversation_id = None
        
        if not conversation_id:
            conversation_id = f"conv_{uuid.uuid4().hex[:12]}"
            self.conversations[conversation_id] = {
                "messages": [],
                "created_at": datetime.now(),
                "last_updated": datetime.now()
            }
        
        return conversation_id
    
    def add_message(self, conversation_id: str, role: str, content: str) -> None:
        """
        Add a message to conversation history
        
        Args:
            conversation_id: Conversation ID
            role: Message role ('user' or 'assistant')
            content: Message content
        """
        if conversation_id not in self.conversations:
            self.get_or_create_conversation(conversation_id)
        
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        
        self.conversations[conversation_id]["messages"].append(message)
        self.conversations[conversation_id]["last_updated"] = datetime.now()
        
        # Limit conversation history
        messages = self.conversations[conversation_id]["messages"]
        if len(messages) > self.max_history * 2:  # *2 because we have user + assistant pairs
            # Keep only the most recent messages
            self.conversations[conversation_id]["messages"] = messages[-self.max_history * 2:]
    
    def get_messages(self, conversation_id: str) -> List[Message]:
        """
        Get all messages for a conversation
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            List of messages
        """
        if conversation_id not in self.conversations:
            return []
        
        return self.conversations[conversation_id]["messages"]
    
    def get_conversation_history_for_openai(self, conversation_id: str) -> List[Dict[str, str]]:
        """
        Get conversation history formatted for OpenAI API
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            List of message dictionaries for OpenAI API
        """
        messages = self.get_messages(conversation_id)
        return [{"role": msg.role, "content": msg.content} for msg in messages]
    
    def get_message_count(self, conversation_id: str) -> int:
        """Get the number of messages in a conversation"""
        if conversation_id not in self.conversations:
            return 0
        return len(self.conversations[conversation_id]["messages"])
    
    def clear_conversation(self, conversation_id: str) -> bool:
        """
        Clear a conversation
        
        Args:
            conversation_id: Conversation ID to clear
            
        Returns:
            True if conversation was cleared, False if not found
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False
    
    def cleanup_old_conversations(self) -> int:
        """
        Remove conversations that have timed out
        
        Returns:
            Number of conversations removed
        """
        now = datetime.now()
        timeout = timedelta(minutes=self.timeout_minutes)
        removed = 0
        
        conversation_ids = list(self.conversations.keys())
        for conv_id in conversation_ids:
            last_updated = self.conversations[conv_id]["last_updated"]
            if now - last_updated > timeout:
                del self.conversations[conv_id]
                removed += 1
        
        return removed


# Global conversation manager instance
conversation_manager = ConversationManager()

