"""
tests/ai/test_groq_client.py

Tests for the Groq API Client.
Verifies failure handling, timeout, and basic instantiation.
"""

import pytest
from unittest.mock import patch, MagicMock
from ai.groq_client import GroqClient

@patch('ai.groq_client.Groq')
def test_timeout_handling(mock_groq_class):
    # Setup mock to raise an exception simulating timeout
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("Timeout")
    mock_groq_class.return_value = mock_client
    
    client = GroqClient()
    
    # We expect the tenacity retry to fail after max attempts
    with pytest.raises(Exception) as excinfo:
        client.generate(system_prompt="sys", user_prompt="usr")
    
    assert "Timeout" in str(excinfo.value)
