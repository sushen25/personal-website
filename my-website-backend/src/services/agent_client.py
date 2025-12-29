"""
Client for communicating with the Agent Service Runtime.
"""

import httpx
import json
import os
import boto3
from typing import Dict, List, Any, Optional

from src.models.schemas import ChatMessage


class AgentClient:
    """Client for invoking the Agent Service via agentcore runtime or HTTP."""

    def __init__(self):
        """Initialize the Agent Client."""
        # Support both local HTTP and deployed Bedrock Agent ARN
        self.agent_url = os.getenv('AGENT_SERVICE_URL', 'http://localhost:8080')
        self.timeout = int(os.getenv('AGENT_TIMEOUT', '30'))  # seconds
        self._http_client = None
        self._bedrock_client = None

        # Determine if we're using Bedrock ARN or HTTP
        self.is_bedrock_arn = self.agent_url.startswith('arn:aws:bedrock')

    def _get_http_client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client (lazy initialization)."""
        if self._http_client is None:
            self._http_client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout),
                follow_redirects=False
            )
        return self._http_client

    def _get_bedrock_client(self):
        """Get or create the Bedrock Agent Core client (lazy initialization)."""
        if self._bedrock_client is None:
            self._bedrock_client = boto3.client('bedrock-agentcore')
        return self._bedrock_client

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
        if self.is_bedrock_arn:
            # Collect all streaming events into a single response
            content_text = ""
            async for event in self._invoke_bedrock_agent_stream(session_id, messages):
                if 'event' in event and 'contentBlockDelta' in event['event']:
                    delta = event['event']['contentBlockDelta'].get('delta', {})
                    content_text += delta.get('text', '')

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
            return await self._invoke_http_agent(session_id, messages)

    async def _invoke_http_agent(
        self,
        session_id: str,
        messages: List[ChatMessage],
    ) -> Dict[str, Any]:
        """Invoke HTTP-based agent (non-streaming)."""
        user_messages = [msg for msg in messages if msg.role == "user"]
        if not user_messages:
            raise Exception("No user message found in messages list")

        latest_user_message = user_messages[-1].content

        payload = {
            "prompt": latest_user_message,
            "session_id": session_id
        }

        try:
            http_client = self._get_http_client()

            response = await http_client.post(
                f"{self.agent_url}/invocations",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code != 200:
                error_detail = response.text
                raise Exception(f"Agent service returned status {response.status_code}: {error_detail}")

            response_data = response.json()

            if "result" in response_data:
                result = response_data["result"]

                content_text = ""
                if isinstance(result, dict):
                    if "content" in result and isinstance(result["content"], list):
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
            response = await http_client.get(
                f"{self.agent_url}/ping",
                timeout=5.0
            )
            return response.status_code == 200
        except Exception:
            try:
                response = await http_client.post(
                    f"{self.agent_url}/invocations",
                    json={"input": {"prompt": "health check"}},
                    timeout=5.0
                )
                return response.status_code == 200
            except Exception:
                return False

    async def invoke_agent_stream(
        self,
        session_id: str,
        messages: List[ChatMessage],
    ):
        """
        Invoke the Agent Service with streaming support.

        Args:
            session_id: Conversation session ID
            messages: List of chat messages

        Yields:
            Dictionary events from the agent as they arrive

        Raises:
            Exception: If agent invocation fails
        """
        if self.is_bedrock_arn:
            async for event in self._invoke_bedrock_agent_stream(session_id, messages):
                yield event
        else:
            async for event in self._invoke_http_agent_stream(session_id, messages):
                yield event

    async def _invoke_bedrock_agent_stream(
        self,
        session_id: str,
        messages: List[ChatMessage],
    ):
        """Stream responses from Bedrock Agent Core."""
        user_messages = [msg for msg in messages if msg.role == "user"]
        if not user_messages:
            raise Exception("No user message found in messages list")

        latest_user_message = user_messages[-1].content

        try:
            bedrock_client = self._get_bedrock_client()

            # Prepare payload for Bedrock Agent Core
            payload = json.dumps({"prompt": latest_user_message}).encode('utf-8')

            # Invoke agent runtime with the full ARN
            response = bedrock_client.invoke_agent_runtime(
                agentRuntimeArn=self.agent_url,
                runtimeSessionId=session_id,
                payload=payload
            )

            # Process streaming response from Bedrock Agent Core
            # The response body contains newline-delimited JSON events
            response_body = response.get('response')

            if response_body:
                # Stream the response line by line using iter_lines
                # boto3 StreamingBody supports iteration
                buffer = ''
                event_count = 0
                for chunk in response_body.iter_chunks(chunk_size=1024):
                    if chunk:
                        # Decode chunk and add to buffer
                        chunk_str = chunk.decode('utf-8') if isinstance(chunk, bytes) else chunk
                        buffer += chunk_str

                        # Process complete lines
                        while '\n' in buffer:
                            line, buffer = buffer.split('\n', 1)
                            line = line.strip()

                            if not line:
                                continue

                            # Remove SSE "data: " prefix if present
                            if line.startswith('data: '):
                                line = line[6:]  # Remove "data: " prefix

                            try:
                                # Each line is a complete JSON object: {"event": {...}}
                                event_data = json.loads(line)

                                # Yield the event directly - it's already in the correct format
                                if 'event' in event_data:
                                    event_count += 1
                                    print(f"Yielding event #{event_count}: {str(event_data)[:100]}")
                                    yield event_data
                            except json.JSONDecodeError as e:
                                print(f"Failed to parse event line: {line} - Error: {e}")
                                continue

                print(f"Total events yielded: {event_count}")

                # Process any remaining data in buffer
                if buffer.strip():
                    line = buffer.strip()
                    if line.startswith('data: '):
                        line = line[6:]
                    try:
                        event_data = json.loads(line)
                        if 'event' in event_data:
                            event_count += 1
                            print(f"Yielding final event #{event_count}: {str(event_data)[:100]}")
                            yield event_data
                    except json.JSONDecodeError:
                        pass

        except Exception as e:
            print(f"Error invoking Bedrock Agent Core: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Failed to invoke Bedrock agent: {str(e)}")

    async def _invoke_http_agent_stream(
        self,
        session_id: str,
        messages: List[ChatMessage],
    ):
        """Stream responses from HTTP-based agent."""
        user_messages = [msg for msg in messages if msg.role == "user"]
        if not user_messages:
            raise Exception("No user message found in messages list")

        latest_user_message = user_messages[-1].content

        payload = {
            "prompt": latest_user_message,
            "session_id": session_id
        }

        try:
            http_client = self._get_http_client()

            async with http_client.stream(
                "POST",
                f"{self.agent_url}/invocations",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=httpx.Timeout(self.timeout)
            ) as response:
                if response.status_code != 200:
                    error_detail = await response.aread()
                    raise Exception(f"Agent service returned status {response.status_code}: {error_detail.decode()}")

                async for line in response.aiter_lines():
                    if line.strip():
                        try:
                            # Handle SSE format - lines are prefixed with "data: "
                            if line.startswith("data: "):
                                line = line[6:]  # Remove "data: " prefix

                            event = json.loads(line)
                            yield event
                        except json.JSONDecodeError as e:
                            print(f"Failed to parse event line: {line}")
                            # Skip invalid JSON lines
                            continue

        except httpx.TimeoutException:
            print(f"Agent service request timed out after {self.timeout}s")
            raise Exception(f"Agent service request timed out after {self.timeout} seconds")

        except httpx.ConnectError as e:
            print(f"Failed to connect to agent service at {self.agent_url}: {str(e)}")
            raise Exception(f"Could not connect to agent service. Is it running at {self.agent_url}?")

        except httpx.HTTPError as e:
            print(f"HTTP error calling agent service: {str(e)}")
            raise Exception(f"Failed to invoke agent service: {str(e)}")

        except Exception as e:
            print(f"Error invoking agent service: {str(e)}")
            raise

    async def close(self):
        """Close the HTTP client connection."""
        if self._http_client is not None:
            await self._http_client.aclose()


# Global instance for reuse
agent_client = AgentClient()
