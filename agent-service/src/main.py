"""
Lambda handler for the Agent Service.

This handler receives requests from the backend API, initializes the Strands Agent,
processes the conversation, and returns the agent's response.
"""

import json
import os
from typing import Dict, Any, List, Optional
from src.agent.personal_assistant import create_personal_assistant
from src.utils.secrets_manager import SecretsManager


# Initialize secrets manager (cached)
secrets_manager = SecretsManager()


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for agent service invocations.

    Expected event format:
    {
        "session_id": "uuid-string",
        "messages": [
            {"role": "user", "content": "What is your background?"},
            {"role": "assistant", "content": "..."}
        ],
        "model_provider": "bedrock" | "openai" | "anthropic" | "gemini"
    }

    Returns:
    {
        "response": "Agent response text",
        "session_id": "uuid-string",
        "model_used": "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0",
        "metadata": {...}
    }
    """
    try:
        # Parse event (could be from Lambda invoke or API Gateway)
        if isinstance(event, str):
            event = json.loads(event)
        
        # Handle API Gateway event format
        if "body" in event:
            body = json.loads(event["body"]) if isinstance(event["body"], str) else event["body"]
        else:
            body = event

        # Extract parameters
        session_id = body.get("session_id", "unknown")
        messages = body.get("messages", [])
        model_provider = body.get("model_provider", "bedrock")

        # Validate input
        if not messages:
            raise ValueError("No messages provided")

        # Get API key if needed (for non-Bedrock providers)
        api_key = None
        if model_provider.lower() != "bedrock":
            secret_name = f"{os.getenv('STAGE', 'dev')}/portfolio/{model_provider}-api-key"
            try:
                api_key = secrets_manager.get_secret(secret_name)
            except Exception as e:
                print(f"Warning: Could not retrieve API key for {model_provider}: {str(e)}")

        # Create agent
        agent = create_personal_assistant(model_provider=model_provider, api_key=api_key)

        # Get the last user message (most recent user input)
        user_messages = [msg for msg in messages if msg.get("role") == "user"]
        if not user_messages:
            raise ValueError("No user messages found")

        last_user_message = user_messages[-1]["content"]

        # Invoke agent with the message
        # Strands Agent processes the message and uses tools as needed
        response = agent.run(last_user_message)

        # Extract response text
        if isinstance(response, str):
            response_text = response
        elif isinstance(response, dict):
            response_text = response.get("content", response.get("response", str(response)))
        else:
            response_text = str(response)

        # Return standardized response
        # Note: When invoked via Lambda invoke API, return dict directly (not API Gateway format)
        # The backend's agent_client will parse response['Payload']
        return {
            "message": {
                "content": response_text,
                "role": "assistant"
            },
            "session_id": session_id,
            "model_used": _get_model_name(model_provider),
            "metadata": {
                "model_provider": model_provider,
                "model_used": _get_model_name(model_provider),
                "message_count": len(messages)
            }
        }

    except ValueError as e:
        # Validation errors - return error dict
        print(f"Validation error in agent handler: {str(e)}")
        raise  # Let Lambda handle the error
    except Exception as e:
        # Other errors - log and re-raise
        print(f"Error in agent handler: {str(e)}")
        import traceback
        traceback.print_exc()
        raise  # Let Lambda handle the error


def _get_model_name(model_provider: str) -> str:
    """Get the full model name for a provider."""
    provider_lower = model_provider.lower()
    
    model_map = {
        "bedrock": "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0",
        "openai": "openai/gpt-4o",
        "anthropic": "anthropic/claude-3-5-sonnet-20241022",
        "gemini": "gemini/gemini-1.5-pro"
    }
    
    return model_map.get(provider_lower, "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0")

