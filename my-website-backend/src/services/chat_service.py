"""
Chat service for managing conversations and agent interactions.
"""

import time
import uuid
from typing import List, Optional
from datetime import datetime
from boto3.dynamodb.conditions import Key

from src.models.schemas import ChatMessage, ChatResponse, ConversationHistory
from src.services.agent_client import agent_client
from src.utils.dynamodb import chat_db
from src.middleware.error_handler import AgentServiceError, NotFoundError


class ChatService:
    """Service for managing chat conversations and agent interactions."""

    async def send_message(
        self,
        session_id: str,
        messages: List[ChatMessage],
    ) -> ChatResponse:
        """
        Send a message to the agent and save the conversation.

        Args:
            session_id: Conversation session ID
            messages: List of chat messages

        Returns:
            ChatResponse with agent's reply and metadata

        Raises:
            AgentServiceError: If agent service fails
        """
        start_time = time.time()

        try:
            # Invoke Agent Service
            agent_response = await agent_client.invoke_agent(
                session_id=session_id,
                messages=messages,
            )

            # Parse agent response
            assistant_message = agent_response.get('message', {})
            metadata = agent_response.get('metadata', {})

            # Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)
            metadata['response_time_ms'] = response_time_ms

            # Create assistant message
            assistant_chat_message = ChatMessage(
                role="assistant",
                content=assistant_message.get('content', ''),
                timestamp=time.time()
            )

            # Save messages to DynamoDB
            await self._save_messages(
                session_id=session_id,
                messages=messages + [assistant_chat_message],
                metadata=metadata
            )

            # Return response
            return ChatResponse(
                session_id=session_id,
                message=assistant_chat_message,
                metadata=metadata
            )

        except Exception as e:
            print(f"Error in send_message: {str(e)}")
            raise AgentServiceError(
                message="Failed to get response from AI assistant",
                detail={"error": str(e)}
            )

    async def get_conversation_history(self, session_id: str) -> ConversationHistory:
        """
        Retrieve conversation history for a session.

        Args:
            session_id: Session identifier

        Returns:
            ConversationHistory with all messages

        Raises:
            NotFoundError: If session not found
        """
        try:
            # Query DynamoDB for all messages in this session
            items = chat_db.query(
                key_condition=Key('sessionId').eq(session_id),
                scan_index_forward=True  # Sort by timestamp ascending
            )

            if not items:
                raise NotFoundError(
                    message=f"Session not found: {session_id}",
                    detail={"session_id": session_id}
                )

            # Convert to ChatMessage objects
            messages = []
            created_at = None
            updated_at = None

            for item in items:
                messages.append(ChatMessage(
                    role=item.get('role'),
                    content=item.get('content'),
                    timestamp=item.get('timestamp')
                ))

                # Track timestamps
                item_timestamp = datetime.fromtimestamp(item.get('timestamp', 0))
                if created_at is None or item_timestamp < created_at:
                    created_at = item_timestamp
                if updated_at is None or item_timestamp > updated_at:
                    updated_at = item_timestamp

            return ConversationHistory(
                session_id=session_id,
                messages=messages,
                created_at=created_at,
                updated_at=updated_at
            )

        except NotFoundError:
            raise
        except Exception as e:
            print(f"Error retrieving conversation history: {str(e)}")
            raise Exception(f"Failed to retrieve conversation: {str(e)}")

    async def delete_conversation(self, session_id: str) -> bool:
        """
        Delete all messages for a session.

        Args:
            session_id: Session identifier

        Returns:
            True if deleted, False if not found
        """
        try:
            # Get all messages for this session
            items = chat_db.query(
                key_condition=Key('sessionId').eq(session_id)
            )

            if not items:
                return False

            # Delete each message
            for item in items:
                chat_db.delete_item({
                    'sessionId': session_id,
                    'timestamp': item.get('timestamp')
                })

            return True

        except Exception as e:
            print(f"Error deleting conversation: {str(e)}")
            raise Exception(f"Failed to delete conversation: {str(e)}")

    async def list_sessions(self, limit: int = 10) -> List[str]:
        """
        List recent session IDs.

        Args:
            limit: Maximum number of sessions to return

        Returns:
            List of session IDs
        """
        try:
            # Scan DynamoDB for unique session IDs
            # Note: In production, consider using a GSI on createdDate for better performance
            items = chat_db.scan(limit=limit * 10)  # Get more to find unique sessions

            # Extract unique session IDs
            session_ids = set()
            for item in items:
                session_ids.add(item.get('sessionId'))
                if len(session_ids) >= limit:
                    break

            return list(session_ids)[:limit]

        except Exception as e:
            print(f"Error listing sessions: {str(e)}")
            return []

    async def send_message_stream(
        self,
        session_id: str,
        messages: List[ChatMessage],
    ):
        """
        Send a message to the agent and stream the response.

        Args:
            session_id: Conversation session ID
            messages: List of chat messages

        Yields:
            Dictionary events from the agent as they arrive

        Raises:
            AgentServiceError: If agent service fails
        """
        start_time = time.time()
        accumulated_content = ""

        try:
            async for event in agent_client.invoke_agent_stream(
                session_id=session_id,
                messages=messages
            ):
                text_delta = None

                if "event" in event:
                    event_data = event["event"]
                    if "contentBlockDelta" in event_data:
                        delta = event_data["contentBlockDelta"].get("delta", {})
                        text_delta = delta.get("text", "")
                elif "data" in event:
                    text_delta = event["data"]

                # Accumulate text content for saving later
                if text_delta:
                    accumulated_content += text_delta

                    # Transform event to simple format for frontend
                    transformed_event = {
                        "data": text_delta,
                        "type": "content_block_delta"
                    }
                    yield transformed_event
                else:
                    yield event

            response_time_ms = int((time.time() - start_time) * 1000)

            assistant_message = ChatMessage(
                role="assistant",
                content=accumulated_content,
                timestamp=time.time()
            )

            metadata = {
                'response_time_ms': response_time_ms,
                'session_id': session_id
            }

            # TODO: Save to DynamoDB
            # await self._save_messages(
            #     session_id=session_id,
            #     messages=messages + [assistant_message],
            #     metadata=metadata
            # )

            yield {
                "complete": True,
                "session_id": session_id
            }

        except Exception as e:
            print(f"Error in send_message_stream: {str(e)}")
            # Yield error event
            yield {
                "error": str(e),
                "session_id": session_id
            }

    async def _save_messages(
        self,
        session_id: str,
        messages: List[ChatMessage],
        metadata: dict = None
    ) -> None:
        """
        Save messages to DynamoDB.

        Args:
            session_id: Session identifier
            messages: List of messages to save
            metadata: Optional metadata to include
        """
        try:
            current_date = datetime.now().strftime('%Y-%m-%d')

            for message in messages:
                # Generate message ID
                message_id = str(uuid.uuid4())

                # Calculate TTL (90 days from now)
                ttl = int(time.time()) + (90 * 24 * 60 * 60)

                # Prepare item
                item = {
                    'sessionId': session_id,
                    'timestamp': message.timestamp or time.time(),
                    'messageId': message_id,
                    'role': message.role,
                    'content': message.content,
                    'createdDate': current_date,
                    'ttl': ttl,
                }

                # Add metadata for assistant messages
                if message.role == 'assistant' and metadata:
                    item['modelUsed'] = metadata.get('model_used', 'unknown')
                    item['tokenCount'] = metadata.get('token_count', 0)
                    item['responseTime'] = metadata.get('response_time_ms', 0)

                # Save to DynamoDB
                chat_db.put_item(item)

        except Exception as e:
            print(f"Error saving messages: {str(e)}")
            # Don't raise - conversation should continue even if save fails


# Global instance for reuse
chat_service = ChatService()
