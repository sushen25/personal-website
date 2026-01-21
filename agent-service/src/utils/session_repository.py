"""
DynamoDB-based session repository for Strands agent framework.
"""

import json
import time
import uuid
from typing import Optional, List
from datetime import datetime

from strands.session.session_repository import SessionRepository
from strands.types.session import Session, SessionAgent, SessionMessage

from boto3.dynamodb.conditions import Key

from utils.dynamodb import chat_db


class DynamoDBSessionRepository(SessionRepository):
    """
    Custom session repository that stores agent sessions in DynamoDB.

    This implementation uses the existing chat conversations table schema:
    - sessionId (partition key)
    - timestamp (sort key)
    - Additional fields: messageId, role, content, agentState, etc.
    """

    def __init__(self):
        """Initialize the DynamoDB session repository."""
        self.db = chat_db

    # Session methods
    def create_session(self, session: Session) -> Session:
        """
        Create a new session in DynamoDB.

        Args:
            session: Session object to create

        Returns:
            The created session
        """
        try:
            current_date = datetime.now().strftime('%Y-%m-%d')
            timestamp = time.time()
            ttl = int(time.time()) + (90 * 24 * 60 * 60)  # 90 days TTL

            # Helper to convert datetime or string to ISO format
            def to_iso_string(dt):
                if dt is None:
                    return datetime.now().isoformat()
                if isinstance(dt, str):
                    return dt
                return dt.isoformat()

            item = {
                'sessionId': session.session_id,
                'timestamp': timestamp,
                'messageId': f"session-{session.session_id}",
                'role': 'system',
                'content': json.dumps({
                    'type': 'session',
                    'session_type': session.session_type,
                    'created_at': to_iso_string(session.created_at),
                    'updated_at': to_iso_string(session.updated_at),
                }),
                'createdDate': current_date,
                'ttl': ttl,
            }

            self.db.put_item(item)
            return session

        except Exception as e:
            print(f"Error creating session: {str(e)}")
            raise

    def read_session(self, session_id: str) -> Optional[Session]:
        """
        Read a session from DynamoDB.

        Args:
            session_id: Session ID to read

        Returns:
            Session object or None if not found
        """
        try:
            # Query for session metadata
            items = self.db.query(
                key_condition=Key('sessionId').eq(session_id),
                limit=1
            )

            if not items:
                return None

            # Parse session data
            item = items[0]
            content = json.loads(item.get('content', '{}'))

            if content.get('type') != 'session':
                # If first item is not session metadata, create default session
                session = Session(
                    session_id=session_id,
                    session_type="default",
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
            else:
                session = Session(
                    session_id=session_id,
                    session_type=content.get('session_type', 'default'),
                    created_at=datetime.fromisoformat(content.get('created_at', datetime.now().isoformat())),
                    updated_at=datetime.fromisoformat(content.get('updated_at', datetime.now().isoformat()))
                )

            return session

        except Exception as e:
            print(f"Error reading session: {str(e)}")
            return None

    # Agent methods
    def create_agent(self, session_id: str, agent: SessionAgent) -> SessionAgent:
        """
        Create/store agent state in DynamoDB.

        Args:
            session_id: Session ID
            agent: SessionAgent object to store

        Returns:
            The created agent
        """
        try:
            current_date = datetime.now().strftime('%Y-%m-%d')
            timestamp = time.time()
            ttl = int(time.time()) + (90 * 24 * 60 * 60)

            item = {
                'sessionId': session_id,
                'timestamp': timestamp,
                'messageId': f"agent-{agent.agent_id}",
                'role': 'system',
                'content': json.dumps({
                    'type': 'agent',
                    'agent_id': agent.agent_id,
                    'state': agent.state or {},
                    'conversation_manager_state': agent.conversation_manager_state or {},
                }),
                'createdDate': current_date,
                'ttl': ttl,
            }

            self.db.put_item(item)
            return agent

        except Exception as e:
            print(f"Error creating agent: {str(e)}")
            raise

    def read_agent(self, session_id: str, agent_id: str) -> Optional[SessionAgent]:
        """
        Read agent state from DynamoDB.

        Args:
            session_id: Session ID
            agent_id: Agent ID

        Returns:
            SessionAgent object or None if not found
        """
        try:
            # Query for all items in session
            items = self.db.query(
                key_condition=Key('sessionId').eq(session_id)
            )

            # Find agent state item
            for item in items:
                content = json.loads(item.get('content', '{}'))
                if content.get('type') == 'agent' and content.get('agent_id') == agent_id:
                    return SessionAgent(
                        agent_id=agent_id,
                        state=content.get('state', {}),
                        conversation_manager_state=content.get('conversation_manager_state', {})
                    )

            return None

        except Exception as e:
            print(f"Error reading agent: {str(e)}")
            return None

    def update_agent(self, session_id: str, agent: SessionAgent) -> SessionAgent:
        """
        Update agent state in DynamoDB.

        Args:
            session_id: Session ID
            agent: SessionAgent object with updated state

        Returns:
            The updated agent
        """
        print("Update agent not needed")

    # Message methods
    def create_message(self, session_id: str, agent_id: str, message: SessionMessage) -> SessionMessage:
        """
        Create a message in DynamoDB.

        Args:
            session_id: Session ID
            agent_id: Agent ID
            message: SessionMessage object to store

        Returns:
            The created message
        """
        try:
            current_date = datetime.now().strftime('%Y-%m-%d')
            timestamp = time.time()
            ttl = int(time.time()) + (90 * 24 * 60 * 60)

            # SessionMessage structure from API docs:
            # - message_id: int (sequential index)
            # - message: Message object (the actual message)
            # - created_at: timestamp

            # Get the actual message object
            actual_message = message.message

            # Determine role from message type
            role = actual_message["role"]

            # Extract content for easy querying
            content = ''
            msg_content = actual_message["content"]
            if isinstance(msg_content, list):
                for block in msg_content:
                    if isinstance(block, dict) and 'text' in block:
                        content += block['text']
                    elif hasattr(block, 'text'):
                        content += block.text
            else:
                content = str(msg_content)

            print("Content")
            print(content)



            # Serialize the complete SessionMessage for proper reconstruction
            # This allows us to restore the full message with all attributes
            message_dict = message.to_dict()

            item = {
                'sessionId': session_id,
                'timestamp': timestamp,
                'messageId': str(message.message_id),  # Store as string in DDB
                'role': role,
                'content': content,  # Store content separately for easy querying
                'messageData': json.dumps(message_dict),  # Store full serialized message
                'createdDate': current_date,
                'ttl': ttl,
                'agentId': agent_id,
            }

            self.db.put_item(item)
            return message

        except Exception as e:
            print(f"Error creating message: {str(e)}")
            print(f"Message attributes: {dir(message)}")
            if hasattr(message, 'message'):
                print(f"Actual message attributes: {dir(message.message)}")
            raise

    def read_message(self, session_id: str, agent_id: str, message_id: int) -> Optional[SessionMessage]:
        """
        Read a specific message from DynamoDB.

        Args:
            session_id: Session ID
            agent_id: Agent ID
            message_id: Message ID (int - sequential index)

        Returns:
            SessionMessage object or None if not found
        """
        try:
            # Query for all messages in session
            items = self.db.query(
                key_condition=Key('sessionId').eq(session_id)
            )

            # Find specific message (compare as string since stored as string)
            message_id_str = str(message_id)
            for item in items:
                if item.get('messageId') == message_id_str and item.get('role') != 'system':
                    # Reconstruct SessionMessage from stored serialized data
                    message_data = item.get('messageData')
                    if message_data:
                        message_dict = json.loads(message_data)
                        print("READ SINGLE MESSAGE")
                        print(message_dict)
                        return SessionMessage.from_dict(message_dict)
                    else:
                        # Fallback: if messageData doesn't exist (old format)
                        return None

            return None

        except Exception as e:
            print(f"Error reading message: {str(e)}")
            return None

    def update_message(self, session_id: str, agent_id: str, message: SessionMessage) -> SessionMessage:
        """
        Update a message in DynamoDB.

        Note: DynamoDB items are immutable, so we need to delete and recreate.

        Args:
            session_id: Session ID
            agent_id: Agent ID
            message: SessionMessage object with updates

        Returns:
            The updated message
        """
        try:
            # For simplicity, we'll create a new version with current timestamp
            # In production, you might want to find and delete the old version
            return self.create_message(session_id, agent_id, message)

        except Exception as e:
            print(f"Error updating message: {str(e)}")
            raise

    def list_messages(
        self,
        session_id: str,
        agent_id: str,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[SessionMessage]:
        """
        List messages for a session with proper reconstruction.

        Args:
            session_id: Session ID
            agent_id: Agent ID
            limit: Optional limit on number of messages
            offset: Number of messages to skip (for pagination)

        Returns:
            List of SessionMessage objects
        """
        try:
            print("Getting messages for session: ", session_id)
            message_items = self.db.query(
                key_condition=Key('sessionId').eq(session_id),
                scan_index_forward=True  # Chronological order
            )


            # Apply offset and limit for pagination
            start_idx = offset
            end_idx = start_idx + limit if limit else len(message_items)
            paginated_items = message_items[start_idx:end_idx]

            # Reconstruct SessionMessage objects from stored serialized data
            messages = []
            for item in paginated_items:
                message_data = item.get('messageData')
                if message_data:
                    try:
                        message_dict = json.loads(message_data)
                        session_message = SessionMessage.from_dict(message_dict)
                        messages.append(session_message)
                    except Exception as e:
                        print(f"Error reconstructing message {item.get('messageId')}: {str(e)}")
                        continue
            
            
            print(messages)
            return messages

        except Exception as e:
            print(f"Error listing messages: {str(e)}")
            return []