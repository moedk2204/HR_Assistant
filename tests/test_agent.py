"""
Integration Tests for HR Assistant Agent
Tests the full agent with LLM and tool calling
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.agent import HRAssistantChat, run_simple_query


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def chat_instance():
    """Create a fresh chat instance for each test"""
    return HRAssistantChat(verbose=False)


# ============================================================================
# TEST: AGENT INITIALIZATION
# ============================================================================

class TestAgentInitialization:
    """Test agent initialization"""
    
    def test_agent_creates_successfully(self, chat_instance):
        """Test that agent initializes without errors"""
        assert chat_instance is not None, "Agent should initialize"
        assert chat_instance.agent is not None, "Agent executor should exist"
    
    def test_agent_has_empty_history(self, chat_instance):
        """Test that new agent has empty chat history"""
        history = chat_instance.get_history()
        assert len(history) == 0, "New agent should have empty history"


# ============================================================================
# TEST: BASIC CONVERSATIONS
# ============================================================================

class TestBasicConversations:
    """Test basic conversational abilities"""
    
    def test_greeting_response(self, chat_instance):
        """Test that agent responds to greetings"""
        response = chat_instance.chat("Hello!")
        assert len(response) > 0, "Agent should respond to greeting"
        assert not response.startswith("Error"), "Should not error on greeting"
    
    def test_help_query(self, chat_instance):
        """Test that agent can explain its capabilities"""
        response = chat_instance.chat("What can you help me with?")
        assert len(response) > 0, "Agent should explain capabilities"
        # Check for HR-related keywords or general helpfulness
        hr_keywords = ["employee", "leave", "interview", "hr", "help", "assist", "task"]
        has_hr_mention = any(keyword in response.lower() for keyword in hr_keywords)
        assert has_hr_mention, "Should mention capabilities"


# ============================================================================
# TEST: CHAT HISTORY
# ============================================================================

class TestChatHistory:
    """Test chat history management"""
    
    def test_history_updates_after_message(self, chat_instance):
        """Test that history is updated after each message"""
        initial_len = len(chat_instance.get_history())
        chat_instance.chat("Hello!")
        new_len = len(chat_instance.get_history())
        
        assert new_len == initial_len + 1, "History should grow by 1"
    
    def test_reset_clears_history(self, chat_instance):
        """Test that reset clears chat history"""
        chat_instance.chat("Hello!")
        chat_instance.chat("How are you?")
        
        chat_instance.reset()
        history = chat_instance.get_history()
        
        assert len(history) == 0, "Reset should clear history"
    
    def test_history_contains_both_sides(self, chat_instance):
        """Test that history contains both user and assistant messages"""
        user_msg = "Hello!"
        chat_instance.chat(user_msg)
        
        history = chat_instance.get_history()
        assert len(history) > 0, "History should not be empty"
        assert history[0][0] == user_msg, "History should contain user message"
        assert history[0][1] is not None, "History should contain assistant response"


# ============================================================================
# TEST: SIMPLE QUERY FUNCTION
# ============================================================================

class TestSimpleQuery:
    """Test the run_simple_query utility function"""
    
    def test_simple_query_returns_string(self):
        """Test that simple query returns a string response"""
        response = run_simple_query("Hello!", verbose=False)
        assert isinstance(response, str), "Response should be a string"
        assert len(response) > 0, "Response should not be empty"


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])