"""
Chat API route handlers.
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import List
import uuid
import json

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
    session_id = request.session_id or str(uuid.uuid4())

    if not request.messages or len(request.messages) == 0:
        raise ValidationError("At least one message is required")

    user_messages = [msg for msg in request.messages if msg.role == "user"]
    if not user_messages:
        raise ValidationError("At least one user message is required")

    try:
        response = await chat_service.send_message(
            session_id=session_id,
            messages=request.messages
        )
        return response

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat message: {str(e)}"
        )


@router.post("/stream")
async def send_message_stream(request: ChatRequest):
    """
    Send a chat message and stream AI assistant response.

    Args:
        request: Chat request with messages and optional session_id

    Returns:
        StreamingResponse with newline-delimited JSON events

    Raises:
        HTTPException: If validation fails
    """
    session_id = request.session_id or str(uuid.uuid4())

    if not request.messages or len(request.messages) == 0:
        raise ValidationError("At least one message is required")

    user_messages = [msg for msg in request.messages if msg.role == "user"]
    if not user_messages:
        raise ValidationError("At least one user message is required")

    async def event_generator():
        """Generate events from the chat service stream"""
        try:
            async for event in chat_service.send_message_stream(
                session_id=session_id,
                messages=request.messages
            ):
                delta = (json.dumps(event) + "\n").encode('utf-8') 
                yield delta
        except Exception as e:
            error_event = {
                "error": str(e),
                "session_id": session_id
            }
            yield (json.dumps(error_event) + "\n").encode('utf-8')

    return StreamingResponse(
        event_generator(),
        media_type="application/x-ndjson",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # Disable buffering in nginx
        }
    )
