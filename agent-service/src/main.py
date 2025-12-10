import asyncio
from agent.personal_assistant import create_personal_assistant

from bedrock_agentcore.runtime import BedrockAgentCoreApp


app = BedrockAgentCoreApp()

# Sync endpoint
# @app.entrypoint
# def invoke(payload):
#     """Process user input and return a response"""
#     user_message = payload.get("prompt", "Hello")

#     agent = create_personal_assistant()
#     result = agent(user_message)

#     return {"result": result.message}

@app.entrypoint
async def invoke(payload):
    """Process user input and return a streaming response"""
    user_message = payload.get("prompt", "Hello")

    agent = create_personal_assistant()
    stream = agent.stream_async(user_message)

    async for event in stream:
        print(event)
        yield event

if __name__ == "__main__":
    app.run()