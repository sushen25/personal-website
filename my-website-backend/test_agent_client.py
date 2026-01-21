#!/usr/bin/env python3
"""
Simple test script to verify agent client integration with agentcore runtime.
Make sure the agent service is running on http://localhost:8080 before running this test.
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.models.schemas import ChatMessage
from src.services.agent_client import AgentClient


async def test_agent_client():
    """Test the agent client with a simple message."""
    print("Testing Agent Client Integration")
    print("=" * 50)

    # Create client
    client = AgentClient()
    print(f"Agent Service URL: {client.agent_url}")
    print()

    # Test 1: Health check
    print("Test 1: Health Check")
    print("-" * 50)
    try:
        is_healthy = await client.check_agent_service_health()
        print(f"✓ Health check: {'PASSED' if is_healthy else 'FAILED'}")
    except Exception as e:
        print(f"✗ Health check failed: {str(e)}")
        return
    print()

    # Test 2: Simple message
    print("Test 2: Send Message")
    print("-" * 50)
    try:
        # Create a test message
        test_message = ChatMessage(
            role="user",
            content="What is your purpose?",
            timestamp=datetime.now().timestamp()
        )

        # Invoke agent
        print(f"Sending message: '{test_message.content}'")
        response = await client.invoke_agent(
            session_id="test-session-123",
            messages=[test_message]
        )

        # Print response
        print(f"✓ Response received")
        print(f"  Message: {response['message']['content'][:100]}...")
        print(f"  Metadata: {response['metadata']}")
    except Exception as e:
        print(f"✗ Message test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    print()

    # Test 3: Conversation with multiple messages
    print("Test 3: Multi-turn Conversation")
    print("-" * 50)
    try:
        messages = [
            ChatMessage(
                role="user",
                content="Who are you?",
                timestamp=datetime.now().timestamp()
            ),
            ChatMessage(
                role="assistant",
                content="I am an AI assistant that can help you learn about Sushen.",
                timestamp=datetime.now().timestamp()
            ),
            ChatMessage(
                role="user",
                content="What skills does Sushen have?",
                timestamp=datetime.now().timestamp()
            )
        ]

        print(f"Sending conversation with {len(messages)} messages")
        response = await client.invoke_agent(
            session_id="test-session-123",
            messages=messages
        )

        print(f"✓ Response received")
        print(f"  Message: {response['message']['content'][:100]}...")
    except Exception as e:
        print(f"✗ Conversation test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    print()

    # Clean up
    await client.close()

    print("=" * 50)
    print("All tests completed successfully! ✓")


if __name__ == "__main__":
    # Set environment variable for local testing
    os.environ.setdefault("AGENT_SERVICE_URL", "http://localhost:8080")

    # Run the async test
    asyncio.run(test_agent_client())
