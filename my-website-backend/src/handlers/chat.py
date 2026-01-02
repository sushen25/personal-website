"""
Chat API route handlers.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import StreamingResponse
from typing import List
import uuid
import json

from src.models.schemas import ChatRequest, ChatResponse, ChatMessage, ConversationHistory
from src.services.chat_service import chat_service
from src.middleware.error_handler import NotFoundError, ValidationError
from src.middleware.rate_limiter import chat_rate_limiter
from src.middleware.auth import verify_api_key

# Create router
router = APIRouter()


@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def send_message(
    chat_request: ChatRequest,
    _rate_limit: None = Depends(chat_rate_limiter.check_rate_limit),
    _api_key: str = Depends(verify_api_key)
) -> ChatResponse:
    """
    Send a chat message and get AI assistant response.

    Args:
        chat_request: Chat request with messages and optional session_id
        _rate_limit: Rate limiting dependency (checks IP-based rate limits)
        _api_key: API key authentication dependency

    Returns:
        ChatResponse with assistant's message and metadata

    Raises:
        HTTPException: If chat service fails, rate limit exceeded, or invalid API key
    """
    session_id = chat_request.session_id or str(uuid.uuid4())

    if not chat_request.messages or len(chat_request.messages) == 0:
        raise ValidationError("At least one message is required")

    user_messages = [msg for msg in chat_request.messages if msg.role == "user"]
    if not user_messages:
        raise ValidationError("At least one user message is required")

    try:
        response = await chat_service.send_message(
            session_id=session_id,
            messages=chat_request.messages
        )
        return response

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat message: {str(e)}"
        )


@router.post("/stream")
async def send_message_stream(
    chat_request: ChatRequest,
    _rate_limit: None = Depends(chat_rate_limiter.check_rate_limit),
    _api_key: str = Depends(verify_api_key)
):
    """
    Send a chat message and stream AI assistant response.

    Args:
        chat_request: Chat request with messages and optional session_id
        _rate_limit: Rate limiting dependency (checks IP-based rate limits)
        _api_key: API key authentication dependency

    Returns:
        StreamingResponse with newline-delimited JSON events

    Raises:
        HTTPException: If validation fails, rate limit exceeded, or invalid API key
    """
    session_id = chat_request.session_id or str(uuid.uuid4())

    if not chat_request.messages or len(chat_request.messages) == 0:
        raise ValidationError("At least one message is required")

    user_messages = [msg for msg in chat_request.messages if msg.role == "user"]
    if not user_messages:
        raise ValidationError("At least one user message is required")

    async def event_generator():
        """Generate events from the chat service stream"""
        try:
            async for event in chat_service.send_message_stream(
                session_id=session_id,
                messages=chat_request.messages
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
