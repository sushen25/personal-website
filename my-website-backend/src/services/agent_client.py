"""
Client for communicating with the Agent Service Runtime.
"""

import httpx
import json
import os
from typing import Dict, List, Any, Optional

from src.models.schemas import ChatMessage


class AgentClient:
    """Client for invoking the Agent Service via agentcore runtime."""

    def __init__(self):
        """Initialize the Agent Client with HTTP client."""
        # Support both local and deployed runtime
        self.agent_url = os.getenv('AGENT_SERVICE_URL', 'http://localhost:8080')
        self.timeout = int(os.getenv('AGENT_TIMEOUT', '30'))  # seconds
        self._http_client = None

    def _get_http_client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client (lazy initialization)."""
        if self._http_client is None:
            self._http_client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout),
                follow_redirects=False
                # verify=False
            )
        return self._http_client

    async def invoke_agent(
        self,
        session_id: str,
        messages: List[ChatMessage],
    ) -> Dict[str, Any]:
        """
        Invoke the Agent Service to process chat messages.

        Args:
            session_id: Conversation session ID
            messages: List of chat messages

        Returns:
            Dictionary with agent response

        Raises:
            Exception: If agent invocation fails
        """
        # Get the latest user message for the prompt
        user_messages = [msg for msg in messages if msg.role == "user"]
        if not user_messages:
            raise Exception("No user message found in messages list")

        latest_user_message = user_messages[-1].content

        # Prepare payload for agentcore runtime
        # The runtime expects: {"input": {"prompt": "..."}}
        payload = {
            "input": {
                "prompt": latest_user_message,
                "session_id": session_id,
            }
        }

        try:
            # Get HTTP client
            http_client = self._get_http_client()

            # Make HTTP POST request to agentcore runtime
            response = await http_client.post(
                f"{self.agent_url}/invocations",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            # Check HTTP status
            if response.status_code != 200:
                error_detail = response.text
                raise Exception(f"Agent service returned status {response.status_code}: {error_detail}")

            # Parse response
            response_data = response.json()

            # The agentcore runtime returns: {"result": {"role": "assistant", "content": [{"text": "..."}]}}
            # We need to transform it to match expected format
            if "result" in response_data:
                result = response_data["result"]

                # Extract text content from the result
                content_text = ""
                if isinstance(result, dict):
                    if "content" in result and isinstance(result["content"], list):
                        # Extract text from content blocks
                        for block in result["content"]:
                            if isinstance(block, dict) and "text" in block:
                                content_text += block["text"]
                    elif "content" in result and isinstance(result["content"], str):
                        content_text = result["content"]
                    elif isinstance(result, str):
                        content_text = result
                elif isinstance(result, str):
                    content_text = result

                return {
                    "message": {
                        "content": content_text or "No response generated",
                        "role": "assistant"
                    },
                    "metadata": {
                        "session_id": session_id
                    }
                }
            else:
                raise Exception("Invalid response format from agent service")

        except httpx.TimeoutException:
            print(f"Agent service request timed out after {self.timeout}s")
            raise Exception(f"Agent service request timed out after {self.timeout} seconds")

        except httpx.ConnectError as e:
            print(f"Failed to connect to agent service at {self.agent_url}: {str(e)}")
            raise Exception(f"Could not connect to agent service. Is it running at {self.agent_url}?")

        except httpx.HTTPError as e:
            print(f"HTTP error calling agent service: {str(e)}")
            raise Exception(f"Failed to invoke agent service: {str(e)}")

        except json.JSONDecodeError as e:
            print(f"Failed to parse agent response: {str(e)}")
            raise Exception("Invalid JSON response from agent service")

        except Exception as e:
            print(f"Error invoking agent service: {str(e)}")
            raise

    async def check_agent_service_health(self) -> bool:
        """
        Check if the Agent Service is available.

        Returns:
            True if service is healthy, False otherwise
        """
        http_client = self._get_http_client()
        try:
            # Try to ping the health endpoint (or just the base URL)
            response = await http_client.get(
                f"{self.agent_url}/ping",
                timeout=5.0
            )
            return response.status_code == 200
        except Exception:
            # If ping endpoint doesn't exist, try invocations with a simple test
            try:
                response = await http_client.post(
                    f"{self.agent_url}/invocations",
                    json={"input": {"prompt": "health check"}},
                    timeout=5.0
                )
                return response.status_code == 200
            except Exception:
                return False

    async def close(self):
        """Close the HTTP client connection."""
        if self._http_client is not None:
            await self._http_client.aclose()


# Global instance for reuse
agent_client = AgentClient()
