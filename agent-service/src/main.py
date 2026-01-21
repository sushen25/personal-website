import asyncio
from agent.personal_assistant import create_personal_assistant

from bedrock_agentcore.runtime import BedrockAgentCoreApp


app = BedrockAgentCoreApp()

# Sync endpoint
# @app.entrypoint
# def invoke(payload):
#     """Process user input and return a response""
#     user_message = payload.get("prompt", "Hello")

#     agent = create_personal_assistant()
#     result = agent(user_message)

#     return {"result": result.message}

@app.entrypoint
async def invoke(payload):
    """Process user input and return a streaming response"""
    print("PAYLOAD: ", payload)
    user_message = payload.get("prompt", "Hello")
    session_id = payload.get("session_id", "default-session")

    agent = create_personal_assistant(session_id)
    stream = agent.stream_async(user_message, session_id=session_id)

    async for event in stream:
        try:
            if isinstance(event, dict):
                clean_event = {}
                if "event" in event:
                    clean_event["event"] = {}
                    event_data = event["event"]

                    if "contentBlockDelta" in event_data:
                        delta_data = event_data["contentBlockDelta"]
                        clean_event["event"]["contentBlockDelta"] = {
                            "delta": delta_data.get("delta", {}),
                            "contentBlockIndex": delta_data.get("contentBlockIndex", 0)
                        }

                    for key in ["contentBlockStart", "contentBlockStop", "messageStart", "messageStop"]:
                        if key in event_data:
                            clean_event["event"][key] = event_data[key]
                if clean_event:
                    yield clean_event

        except Exception as e:
            # Log but don't crash on malformed events
            print(f"Error processing event: {e}")
            continue

if __name__ == "__main__":
    app.run()