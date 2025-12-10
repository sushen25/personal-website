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


@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
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
            messages=request.messages
        )
        return response

    except Exception as e:
        # Log error and raise HTTP exception
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat message: {str(e)}"
        )
