# Architecture Decision: Microservices Separation

## Problem

The Strands Agents SDK requires `anyio>=4.0`, which conflicts with FastAPI, OpenAI, and Anthropic libraries that require `anyio<4.0`. Installing both in the same environment causes dependency conflicts.

## Solution

Separate the backend into **two independent Lambda functions** with isolated dependencies:

### 1. Backend API Service (`my-website-backend/`)
**Purpose**: Main FastAPI application
**Dependencies**: FastAPI, boto3, Pydantic (anyio <4.0)
**Responsibilities**:
- Handle HTTP requests from frontend
- Manage DynamoDB operations (chat history, blog posts)
- Orchestrate chat workflow
- Invoke Agent Service
- Return responses to frontend

### 2. Agent Service (`agent-service/`)
**Purpose**: Strands Agent execution
**Dependencies**: strands-agents, strands-agents-tools, boto3 (anyio >=4.0)
**Responsibilities**:
- Run Strands Agent framework
- Execute custom tools
- Call LLM providers (Bedrock, OpenAI, Anthropic)
- Return structured responses

## Communication

The Backend API invokes the Agent Service using:
- **Option 1**: AWS Lambda Invoke API (synchronous, no API Gateway needed)
- **Option 2**: Internal HTTP endpoint (if using API Gateway)

```python
# Backend API invokes Agent Service
import boto3

lambda_client = boto3.client('lambda')
response = lambda_client.invoke(
    FunctionName='agent-service-dev-agent',
    InvocationType='RequestResponse',
    Payload=json.dumps({
        'session_id': session_id,
        'messages': messages,
        'model_provider': 'bedrock'
    })
)
```

## Benefits

1. **Dependency Isolation**: Each service has independent dependencies
2. **Independent Scaling**: Agent service can scale based on AI workload
3. **Easier Maintenance**: Update Strands SDK without affecting main API
4. **Cost Optimization**: Agent Lambda only runs when AI inference is needed
5. **Fault Isolation**: Agent service failures don't crash the main API
6. **Better Testing**: Test services independently

## Deployment

Both services are deployed independently:

```bash
# Deploy Backend API
cd my-website-backend
serverless deploy --stage dev

# Deploy Agent Service
cd ../agent-service
serverless deploy --stage dev
```

## Directory Structure

```
my-website/
├── my-website-frontend/       # Next.js frontend
├── my-website-backend/        # FastAPI backend Lambda
│   ├── src/
│   │   ├── handlers/          # API routes
│   │   ├── services/          # Business logic
│   │   │   ├── chat_service.py
│   │   │   ├── agent_client.py  # ← Invokes Agent Service
│   │   │   └── content_service.py
│   │   ├── utils/             # DynamoDB, Secrets Manager
│   │   └── main.py
│   └── requirements.txt       # FastAPI dependencies
└── agent-service/             # Strands Agent Lambda
    ├── src/
    │   ├── agent/
    │   │   └── personal_assistant.py
    │   ├── tools/             # Custom @tool functions
    │   │   ├── profile_tools.py
    │   │   ├── blog_tools.py
    │   │   └── project_tools.py
    │   └── main.py            # Lambda handler
    └── requirements.txt       # Strands dependencies
```

## Cost Impact

**Minimal cost increase**:
- Agent Service only runs when chat requests occur
- Lambda cold starts: 1-2 seconds (acceptable for chat)
- No additional API Gateway needed (use Lambda Invoke)
- Estimated additional cost: <$1/month for dev environment

## Implementation Priority

1. Complete Backend API implementation (Phase 2)
2. Create Agent Service structure (Phase 2b - new)
3. Implement Agent Service tools and logic
4. Test integration between services
5. Deploy both services

## Future Enhancements

- Add message queue (SQS) for async agent responses
- Implement agent result caching
- Add observability across both services
- Multi-agent patterns (specialized agents for different topics)
