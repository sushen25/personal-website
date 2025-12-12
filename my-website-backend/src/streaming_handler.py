"""
Streaming handler for AWS Lambda Response Streaming.
This handler supports Lambda's response streaming mode for real-time chat responses.
"""

import json
import asyncio
from typing import AsyncIterator
import uuid

from src.models.schemas import ChatRequest
from src.services.chat_service import chat_service
from src.middleware.error_handler import ValidationError


async def stream_chat_response(event: dict) -> AsyncIterator[bytes]:
    """
    Stream chat response from the agent service.

    Args:
        event: Lambda event containing the request

    Yields:
        Bytes chunks of newline-delimited JSON events
    """
    try:
        # Parse request body
        body = json.loads(event.get("body", "{}"))
        request = ChatRequest(**body)

        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())

        # Validate messages
        if not request.messages or len(request.messages) == 0:
            error_data = {"error": "At least one message is required", "session_id": session_id}
            yield (json.dumps(error_data) + "\n").encode('utf-8')
            return

        user_messages = [msg for msg in request.messages if msg.role == "user"]
        if not user_messages:
            error_data = {"error": "At least one user message is required", "session_id": session_id}
            yield (json.dumps(error_data) + "\n").encode('utf-8')
            return

        # Stream response from chat service
        async for event in chat_service.send_message_stream(
            session_id=session_id,
            messages=request.messages
        ):
            yield (json.dumps(event) + "\n").encode('utf-8')

    except ValidationError as e:
        error_data = {"error": str(e), "type": "validation_error"}
        yield (json.dumps(error_data) + "\n").encode('utf-8')
    except Exception as e:
        error_data = {"error": f"Internal server error: {str(e)}", "type": "server_error"}
        yield (json.dumps(error_data) + "\n").encode('utf-8')


def handler(event, context):
    """
    Lambda handler with response streaming support.

    This handler is designed for Lambda's RESPONSE_STREAM invoke mode.
    It uses the response_stream from context to write chunks.
    """
    # Get response stream from Lambda context
    # In RESPONSE_STREAM mode, Lambda provides a response_stream object
    response_stream = getattr(context, 'response_stream', None)

    if not response_stream:
        # Fallback for non-streaming invocations or local testing
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"error": "Response streaming not available"})
        }

    # Set response headers for streaming
    response_stream.set_metadata({
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/x-ndjson",
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Api-Key",
        }
    })

    # Run the async streaming function and write to response stream
    async def write_stream():
        try:
            async for chunk in stream_chat_response(event):
                response_stream.write(chunk)
        except Exception as e:
            error_chunk = (json.dumps({"error": str(e)}) + "\n").encode('utf-8')
            response_stream.write(error_chunk)

    # Execute the async function
    asyncio.run(write_stream())
