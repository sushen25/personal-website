from agent.personal_assistant import create_personal_assistant

from bedrock_agentcore.runtime import BedrockAgentCoreApp


app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload):
    """Process user input and return a response"""
    print("PAYLOAD: ", payload)

    user_message = payload.get("prompt", "Hello")

    print("User message")
    print(user_message)

    agent = create_personal_assistant()
    result = agent(user_message)

    return {"result": result.message}

if __name__ == "__main__":
    app.run()