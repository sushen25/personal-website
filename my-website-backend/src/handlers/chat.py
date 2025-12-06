"""
Chat API route handlers.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid

from src.models.schemas import ChatRequest, ChatResponse, ChatMessage, ConversationHistory
from src.services.chat_service import chat_service
from src.middleware.error_handler import NotFoundError, ValidationError

# Create router
router = APIRouter()


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def send_message(request: ChatRequest) -> ChatResponse:
    """
    Send a chat message and get AI assistant response.

    Args:
        request: Chat request with messages and optional session_id

    Returns:
        ChatResponse with assistant's message and metadata

    Raises:
        HTTPException: If chat service fails
    """
    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())

    # Validate messages
    if not request.messages or len(request.messages) == 0:
        raise ValidationError("At least one message is required")

    # Get the last user message
    user_messages = [msg for msg in request.messages if msg.role == "user"]
    if not user_messages:
        raise ValidationError("At least one user message is required")

    try:
        # Send message to chat service
        response = await chat_service.send_message(
            session_id=session_id,
            messages=request.messages,
            model_provider=request.model_provider or "bedrock"
        )

        return response

    except Exception as e:
        # Log error and raise HTTP exception
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat message: {str(e)}"
        )


@router.get("/session/{session_id}", response_model=ConversationHistory, status_code=status.HTTP_200_OK)
async def get_conversation_history(session_id: str) -> ConversationHistory:
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
        history = await chat_service.get_conversation_history(session_id)

        if not history or len(history.messages) == 0:
            raise NotFoundError(
                message=f"No conversation found for session: {session_id}",
                detail={"session_id": session_id}
            )

        return history

    except NotFoundError:
        raise
    except Exception as e:
        print(f"Error retrieving conversation history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve conversation history: {str(e)}"
        )


@router.delete("/session/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(session_id: str):
    """
    Delete a conversation session.

    Args:
        session_id: Session identifier

    Returns:
        204 No Content on success
    """
    try:
        success = await chat_service.delete_conversation(session_id)

        if not success:
            raise NotFoundError(
                message=f"Session not found: {session_id}",
                detail={"session_id": session_id}
            )

        return None

    except NotFoundError:
        raise
    except Exception as e:
        print(f"Error deleting conversation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete conversation: {str(e)}"
        )


@router.get("/sessions", response_model=List[str], status_code=status.HTTP_200_OK)
async def list_sessions(limit: int = 10) -> List[str]:
    """
    List recent session IDs.

    Args:
        limit: Maximum number of sessions to return

    Returns:
        List of session IDs
    """
    try:
        sessions = await chat_service.list_sessions(limit=limit)
        return sessions

    except Exception as e:
        print(f"Error listing sessions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list sessions: {str(e)}"
        )
