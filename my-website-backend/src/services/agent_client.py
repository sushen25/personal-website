"""
Client for communicating with the Agent Service Lambda.
"""

import boto3
import json
import os
from typing import Dict, List, Any, Optional
from botocore.exceptions import ClientError

from src.models.schemas import ChatMessage


class AgentClient:
    """Client for invoking the Agent Service Lambda function."""

    def __init__(self):
        """Initialize the Agent Client with Lambda client."""
        self.lambda_client = boto3.client('lambda', region_name=os.getenv('AWS_REGION', 'ap-southeast-2'))
        self.agent_function_name = os.getenv('AGENT_FUNCTION_NAME', 'agent-service-dev-agent')
        self.timeout = int(os.getenv('AGENT_TIMEOUT', '30'))  # seconds

    async def invoke_agent(
        self,
        session_id: str,
        messages: List[ChatMessage],
        model_provider: str = "bedrock"
    ) -> Dict[str, Any]:
        """
        Invoke the Agent Service to process chat messages.

        Args:
            session_id: Conversation session ID
            messages: List of chat messages
            model_provider: AI model provider (bedrock, openai, anthropic)

        Returns:
            Dictionary with agent response

        Raises:
            Exception: If agent invocation fails
        """
        # Prepare payload
        payload = {
            "session_id": session_id,
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp
                }
                for msg in messages
            ],
            "model_provider": model_provider
        }

        try:
            # Invoke Lambda function synchronously
            response = self.lambda_client.invoke(
                FunctionName=self.agent_function_name,
                InvocationType='RequestResponse',  # Synchronous invocation
                Payload=json.dumps(payload)
            )

            # Parse response
            response_payload = json.loads(response['Payload'].read())

            # Check for Lambda errors
            if 'FunctionError' in response:
                error_msg = response_payload.get('errorMessage', 'Unknown error')
                raise Exception(f"Agent service error: {error_msg}")

            # Check for application errors in response
            if 'error' in response_payload:
                raise Exception(f"Agent error: {response_payload.get('message', 'Unknown error')}")

            return response_payload

        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_msg = e.response['Error']['Message']
            print(f"AWS Lambda ClientError: {error_code} - {error_msg}")

            if error_code == 'ResourceNotFoundException':
                raise Exception(f"Agent service function not found: {self.agent_function_name}")
            elif error_code == 'TooManyRequestsException':
                raise Exception("Agent service is currently overloaded. Please try again.")
            else:
                raise Exception(f"Failed to invoke agent service: {error_msg}")

        except json.JSONDecodeError as e:
            print(f"Failed to parse agent response: {str(e)}")
            raise Exception("Invalid response from agent service")

        except Exception as e:
            print(f"Error invoking agent service: {str(e)}")
            raise

    def invoke_agent_async(
        self,
        session_id: str,
        messages: List[ChatMessage],
        model_provider: str = "bedrock"
    ) -> str:
        """
        Invoke the Agent Service asynchronously (fire and forget).

        Args:
            session_id: Conversation session ID
            messages: List of chat messages
            model_provider: AI model provider

        Returns:
            Request ID for tracking

        Raises:
            Exception: If invocation fails
        """
        payload = {
            "session_id": session_id,
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp
                }
                for msg in messages
            ],
            "model_provider": model_provider
        }

        try:
            response = self.lambda_client.invoke(
                FunctionName=self.agent_function_name,
                InvocationType='Event',  # Asynchronous invocation
                Payload=json.dumps(payload)
            )

            # Get request ID for tracking
            request_id = response.get('ResponseMetadata', {}).get('RequestId', 'unknown')
            return request_id

        except ClientError as e:
            error_msg = e.response['Error']['Message']
            raise Exception(f"Failed to invoke agent service async: {error_msg}")

    def check_agent_service_health(self) -> bool:
        """
        Check if the Agent Service is available.

        Returns:
            True if service is healthy, False otherwise
        """
        try:
            # Try to get function configuration
            self.lambda_client.get_function_configuration(
                FunctionName=self.agent_function_name
            )
            return True
        except ClientError:
            return False


# Global instance for reuse
agent_client = AgentClient()
