# Backend Implementation Plan for Portfolio Website

## Overview

Build a serverless backend using **FastAPI + Mangum** on **AWS Lambda** with **DynamoDB** for data persistence. The backend will handle AI chat requests, serve dynamic content, and track analytics.

## Architecture Summary

### Technology Stack
- **Backend Framework**: FastAPI with Mangum (ASGI adapter for Lambda)
- **Language**: Python 3.11
- **Database**: DynamoDB (serverless, pay-per-request)
- **Deployment**: Serverless Framework
- **Cloud Provider**: AWS Lambda (ap-southeast-2 region)
- **AI Providers**: OpenAI, Gemini, Claude (existing support)

### Directory Structure
```
my-website/
├── my-website-frontend/          # Existing Next.js frontend
└── my-website-backend/           # NEW - Serverless backend
    ├── src/
    │   ├── handlers/              # API route handlers
    │   ├── services/              # Business logic
    │   ├── models/                # Pydantic models
    │   ├── middleware/            # FastAPI middleware
    │   ├── utils/                 # Utilities (DynamoDB, Secrets Manager)
    │   └── main.py                # Main FastAPI app + Lambda handler
    ├── scripts/                   # Database seeding scripts
    ├── serverless.yml             # Infrastructure as code
    ├── requirements.txt           # Python dependencies
    └── .python-version            # Python version specification
```

## Database Design

### 1. Chat Conversations Table
**Table Name**: `{stage}-portfolio-chat-conversations`

**Schema**:
- Partition Key: `sessionId` (string) - UUID for each chat session
- Sort Key: `timestamp` (number) - Message ordering
- Attributes: `messageId`, `role`, `content`, `modelUsed`, `tokenCount`, `responseTime`, `createdAt`, `ttl` (90 days)
- GSI: `CreatedDateIndex` on `createdDate` + `timestamp`

**Use Cases**: Store chat history, analytics on AI usage, conversation retrieval

### 2. Blog Posts Table
**Table Name**: `{stage}-portfolio-blog-posts`

**Schema**:
- Partition Key: `postId` (string)
- Attributes: `slug`, `title`, `content`, `excerpt`, `author`, `publishedDate`, `status`, `tags`, `viewCount`, `seoMetadata`
- GSI1: `StatusPublishedDateIndex` on `status` + `publishedDate`
- GSI2: `SlugIndex` on `slug`

**Use Cases**: Dynamic blog post management (future migration from static HTML)

### 3. Analytics Table (TODO Later)
**Table Name**: `{stage}-portfolio-analytics`

**Schema**:
- Partition Key: `metricType` (string) - "pageview" | "chatInteraction" | "apiCall" | "error"
- Sort Key: `timestamp` (number)
- Attributes: `eventId`, `data` (object), `createdAt`, `ttl` (365 days)
- GSI: `DateIndex` on `date` + `timestamp`

**Use Cases**: Track website metrics, chat usage, error monitoring

## API Endpoints

### Chat API
- `POST /api/chat` - Send message, get AI response (with session management)
- `GET /api/chat/session/:sessionId` - Retrieve conversation history

### Blog API (Future)
- `GET /api/blog/posts` - List all published posts
- `GET /api/blog/posts/:slug` - Get single post by slug
- `POST /api/blog/posts/:postId/view` - Increment view count

### Analytics API (Future)
- `POST /api/analytics/event` - Track analytics event

## Critical Files to Create/Modify

### Backend (New Files)

1. **`/my-website-backend/serverless.yml`**
   - Define DynamoDB tables with CloudFormation
   - Configure Lambda function with API Gateway
   - Set IAM permissions for DynamoDB and Secrets Manager
   - Environment variables for table names
   - Python runtime configuration

2. **`/my-website-backend/src/main.py`**
   - FastAPI app setup with routes
   - Mangum wrapper for Lambda
   - Global middleware (CORS, error handling)

3. **`/my-website-backend/src/services/chat_service.py`**
   - AI chat logic (OpenAI/Gemini/Claude integration)
   - Session management and message persistence
   - Fetch API keys from AWS Secrets Manager
   - Get user context from DynamoDB instead of hardcoded file

4. **`/my-website-backend/src/services/content_service.py`**
   - Format content for AI chatbot system prompt

5. **`/my-website-backend/src/utils/secrets_manager.py`**
   - AWS Secrets Manager client with caching
   - Retrieve OpenAI/Gemini/Claude API keys securely

6. **`/my-website-backend/src/utils/dynamodb.py`**
   - DynamoDB client setup using boto3
   - Helper functions for common operations

7. **`/my-website-backend/src/middleware/error_handler.py`**
   - Centralized error handling
   - Structured error responses

8. **`/my-website-backend/src/models/schemas.py`**
   - Pydantic models for request/response validation
   - Type definitions for chat messages, sessions, etc.

9. **`/my-website-backend/scripts/migrate_user_context.py`**
   - One-time migration script
   - Migrate data from `/my-website-frontend/src/lib/userContext.ts` to DynamoDB

### Frontend (Modified Files)

9. **`/my-website-frontend/.env.local`**
   - Add `NEXT_PUBLIC_API_URL` with backend API Gateway URL
   - Update `NEXT_PUBLIC_CHAT_API_URL` to point to new backend

10. **`/my-website-frontend/api/chat.ts`** (CRITICAL SECURITY FIX)
   - **REMOVE hardcoded API key on line 41** (security vulnerability)
   - This file can be deprecated once backend is deployed

## Implementation Steps

### Phase 1: Backend Infrastructure Setup

**Step 1.1: Create Backend Directory**
```bash
cd /Users/sushensatturu/PersonalRepos/my-website/
mkdir my-website-backend
cd my-website-backend
```

**Step 1.2: Set Python Version**
```bash
echo "3.11" > .python-version
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Step 1.3: Create Requirements File**
Create `requirements.txt` with core dependencies:
```
fastapi==0.104.1
mangum==0.17.0
boto3==1.34.0
pydantic==2.5.0
python-dotenv==1.0.0
openai==1.3.0
google-generativeai==0.3.0
anthropic==0.7.0
uvicorn[standard]==0.24.0
```

**Step 1.4: Install Dependencies**
```bash
pip install -r requirements.txt
pip install --dev serverless
npm install -g serverless
```

**Step 1.5: Install Serverless Plugins**
```bash
serverless plugin install -n serverless-python-requirements
serverless plugin install -n serverless-offline
```

**Step 1.6: Create Serverless Configuration**
- Create `serverless.yml` with:
  - Provider: AWS, runtime python3.11, region ap-southeast-2
  - Single Lambda function with `/{proxy+}` route
  - 3 DynamoDB tables (chat conversations, blog posts, analytics)
  - IAM permissions for DynamoDB and Secrets Manager
  - Environment variables for table names
  - Python requirements packaging

**Step 1.7: Deploy Infrastructure**
```bash
serverless deploy --stage dev --verbose
```
This creates all DynamoDB tables and Lambda function.

### Phase 2: Core Backend Implementation

**Step 2.1: FastAPI App Setup (`src/main.py`)**
- Create FastAPI app with routes for chat, blog, analytics
- Add CORS middleware (allow `https://sushensatturu.com`, `http://localhost:3000`)
- Add error handler middleware
- Wrap with Mangum and export handler for Lambda
- Health check endpoint

**Step 2.2: Pydantic Models (`src/models/schemas.py`)**
- Define request/response models with Pydantic
- ChatMessage, ChatRequest, ChatResponse
- BlogPost, AnalyticsEvent models
- Automatic validation and serialization

**Step 2.3: DynamoDB Utilities (`src/utils/dynamodb.py`)**
- Initialize boto3 DynamoDB client and resource
- Helper functions for common operations (get_item, put_item, query, scan)
- Export reusable client instance

**Step 2.4: Secrets Manager (`src/utils/secrets_manager.py`)**
- Create SecretsManager class with caching (5-minute TTL)
- Method: `get_secret(secret_name)` → fetches from AWS and caches
- Thread-safe caching implementation

**Step 2.5: Content Service (`src/services/content_service.py`)**
- `format_for_chatbot()` - Format content as system prompt (similar to existing `formatUserContextForPrompt()`)
- Query DynamoDB for user context data

**Step 2.6: Chat Service (`src/services/chat_service.py`)**
- `send_message(session_id, messages)`:
  1. Get user context from DynamoDB (not hardcoded file)
  2. Fetch API key from Secrets Manager
  3. Call AI provider (OpenAI/Gemini/Claude) with async
  4. Save user message and AI response to DynamoDB
  5. Return AI response with metadata
- `get_conversation_history(session_id)` - Query DynamoDB for session

**Step 2.7: Chat Routes (`src/handlers/chat.py`)**
- FastAPI router with routes:
  - `POST /api/chat` - Validate request with Pydantic, call chat_service.send_message()
  - `GET /api/chat/session/{session_id}` - Call chat_service.get_conversation_history()
- Automatic request validation with Pydantic models

**Step 2.8: Error Handler Middleware**
- Create custom exception classes (AppError, NotFoundError, ValidationError)
- Global exception handler to catch all errors
- Return structured JSON error responses with proper status codes

### Phase 3: AWS Configuration

**Step 3.1: Store API Keys in Secrets Manager**
```bash
aws secretsmanager create-secret \
  --name dev/portfolio/openai-api-key \
  --secret-string "your-actual-openai-key" \
  --region ap-southeast-2
```

**Step 3.2: Deploy Backend**
```bash
cd /Users/sushensatturu/PersonalRepos/my-website/my-website-backend
serverless deploy --stage dev --verbose
```
Save the API Gateway URL from output (e.g., `https://abc123.execute-api.ap-southeast-2.amazonaws.com/dev`)

### Phase 4: Database Migration

**Step 4.1: Create Migration Script (`scripts/migrate_user_context.py`)**
- Parse existing `getUserContext()` data from frontend
- Insert each content type into DynamoDB:
  - About → `contentType: "about", itemId: "main"`
  - Experience → `contentType: "experience", itemId: <uuid>` (2 items)
  - Education → `contentType: "education", itemId: <uuid>` (2 items)
  - Skills → `contentType: "skills", itemId: <uuid>` (each skill)
  - Projects → `contentType: "projects", itemId: <uuid>` (3 items)

**Step 4.2: Run Migration**
```bash
python scripts/migrate_user_context.py
```

**Step 4.3: Verify Data**
```bash
aws dynamodb scan --table-name dev-portfolio-chat-conversations --region ap-southeast-2 --max-items 5
```

### Phase 5: Frontend Integration

**Step 5.1: Update Environment Variables**
Edit `/my-website-frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=https://abc123.execute-api.ap-southeast-2.amazonaws.com/dev
NEXT_PUBLIC_CHAT_API_URL=https://abc123.execute-api.ap-southeast-2.amazonaws.com/dev/api/chat
```

**Step 5.2: Remove Hardcoded API Key (SECURITY FIX)**
In `/my-website-frontend/api/chat.ts`:
- **DELETE line 41** (hardcoded OpenAI API key)
- Change line 40 to: `const apiKey = process.env.OPENAI_API_KEY || process.env.GEMINI_API_KEY || process.env.CLAUDE_API_KEY;`

**Step 5.3: Test Locally**
- Start frontend: `cd my-website-frontend && npm run dev`
- Test chatbot in browser at `http://localhost:3000`
- Verify chat requests go to new backend API

**Step 5.4: Deploy Frontend**
```bash
cd /my-website-frontend
npm run build
npx serverless client deploy --stage dev
```

### Phase 6: Analytics Implementation (Optional - Can be done later)

**Step 6.1: Analytics Service (`src/services/analytics_service.py`)**
- `track_event(metric_type, data)` - Insert event to DynamoDB
- `get_summary(start_date, end_date)` - Query and aggregate metrics
- Async implementation for better performance

**Step 6.2: Analytics Routes (`src/handlers/analytics.py`)**
- FastAPI router with:
  - `POST /api/analytics/event` - Track event
  - `GET /api/analytics/summary` - Get aggregated metrics

**Step 6.3: Frontend Analytics**
- Add analytics tracking to Next.js pages
- Track page views, chat interactions

### Phase 7: Testing & Monitoring

**Step 7.1: Local Testing**
```bash
# Terminal 1: Backend (Option 1 - Uvicorn)
cd my-website-backend
source venv/bin/activate
uvicorn src.main:app --reload --port 8000

# Terminal 1: Backend (Option 2 - Serverless Offline)
cd my-website-backend
serverless offline start

# Terminal 2: Frontend
cd my-website-frontend
npm run dev
```

**Step 7.2: Test Endpoints**
```bash
# Health check
curl https://abc123.execute-api.ap-southeast-2.amazonaws.com/dev/health

# Chat
curl -X POST https://abc123.execute-api.ap-southeast-2.amazonaws.com/dev/api/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "What is Sushen'\''s current role?"}]}'

# Content
curl https://abc123.execute-api.ap-southeast-2.amazonaws.com/dev/api/content/experience
```

**Step 7.3: Monitor Logs**
```bash
serverless logs --function api --stage dev --tail
```

**Step 7.4: Check DynamoDB**
- Verify chat messages are being saved
- Check conversation history retrieval works

## MCP Server Integration (Future)

The architecture is designed to support MCP (Model Context Protocol) integration:

1. Create `src/services/mcp_service.py` with MCP client
2. Register portfolio content as MCP context sources
3. Enable external AI agents to query portfolio data
4. Potential use cases:
   - Resume generation from context
   - Personalized cover letters
   - Interview preparation assistance

## Security Considerations

### Immediate Actions
1. **Remove hardcoded API key** from `/my-website-frontend/api/chat.ts:41` (CRITICAL)
2. Store all API keys in AWS Secrets Manager
3. Never commit `.env` files with secrets

### Implemented Security
- CORS: Whitelist specific origins (sushensatturu.com, localhost:3000)
- Input Validation: Pydantic models for all API inputs with automatic validation
- Type Safety: Python type hints throughout codebase
- Rate Limiting: DynamoDB-backed rate limiter (future enhancement)
- API Key Management: AWS Secrets Manager with 5-minute cache
- Error Handling: Never expose stack traces or internal errors to clients
- HTTPS: Enforced by API Gateway
- Dependency Security: Regular updates via pip and dependabot

## Cost Estimation

### Development Environment (~$3-5/month)
- DynamoDB: $1-2 (on-demand, low traffic)
- Lambda: $0 (free tier)
- API Gateway: $0 (free tier)
- Secrets Manager: $1.20 (3 secrets)
- CloudWatch Logs: $0.50

### Production Environment (~$20-30/month)
- 10x traffic estimation
- DynamoDB: $10-15
- Lambda: $5
- API Gateway: $3
- Secrets Manager: $1.20
- CloudWatch: $2

## Deployment Checklist

Before deployment:
- [ ] AWS credentials configured (`aws configure --profile default`)
- [ ] Serverless Framework installed (`npm install -g serverless`)
- [ ] Python 3.11 installed and virtual environment activated
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Secrets stored in AWS Secrets Manager
- [ ] serverless.yml configured with Python runtime
- [ ] serverless-python-requirements plugin installed
- [ ] Python code linted without errors (`ruff check` or `flake8`)

After deployment:
- [ ] DynamoDB tables created successfully
- [ ] Lambda function deployed
- [ ] API Gateway endpoint accessible
- [ ] User content migrated to DynamoDB
- [ ] Frontend environment variables updated
- [ ] Hardcoded API key removed from code
- [ ] Chat functionality tested end-to-end
- [ ] CloudWatch logs verified

## Rollback Plan

If issues occur:
1. Frontend can continue using existing `/api/chat.ts` serverless function temporarily
2. DynamoDB data persists independently
3. Roll back Lambda deployment: `serverless rollback --timestamp <timestamp>`
4. Frontend environment variables can be reverted to use old endpoints

## Next Steps After MVP

1. **Admin Dashboard**: Build UI for managing blog posts and content
2. **Blog Migration**: Move static blog posts to DynamoDB
3. **Advanced Analytics**: Dashboard for viewing metrics
4. **Authentication**: Add JWT-based auth for admin endpoints (using python-jose)
5. **Rate Limiting**: Implement distributed rate limiting with DynamoDB
6. **MCP Integration**: Connect to MCP server for AI agent context
7. **Automated Testing**: Unit tests with pytest, integration tests with httpx
8. **CI/CD Pipeline**: GitHub Actions for automated deployment
9. **Type Checking**: Add mypy for static type checking
10. **API Documentation**: Automatic OpenAPI docs via FastAPI (available at /docs)

## Summary

This plan creates a production-ready serverless backend using **FastAPI** that:
- ✅ Handles AI chat requests with session persistence (async support for better performance)
- ✅ Serves dynamic content from DynamoDB
- ✅ Tracks analytics and usage metrics
- ✅ Deploys to AWS Lambda with easy one-command deployment
- ✅ Fixes critical security vulnerability (hardcoded API key)
- ✅ Scales automatically with pay-per-use pricing
- ✅ Supports future MCP server integration
- ✅ Maintains existing frontend functionality
- ✅ Automatic API documentation via OpenAPI/Swagger at `/docs`
- ✅ Type safety with Pydantic models and Python type hints
- ✅ Fast performance with async/await support
- ✅ Built-in request/response validation

**Why FastAPI?**
- Modern async Python framework perfect for serverless
- Automatic request/response validation with Pydantic
- Built-in OpenAPI documentation (view at `/docs`)
- Excellent performance (comparable to Node.js/Go)
- Great developer experience with type hints
- Native support for async AI API calls

**Estimated Implementation Time**: 2-3 days for MVP (chat + content APIs)
**Estimated Cost**: $3-5/month (dev), $20-30/month (prod)
