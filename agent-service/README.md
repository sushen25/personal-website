# Agent Service

Strands Agents-based AI assistant service for the portfolio website, deployed as a serverless Lambda function on AWS.

## Overview

This service provides the AI agent that powers the portfolio chatbot. It uses the Strands Agents SDK to orchestrate LLM interactions with custom tools for querying portfolio content (profile, skills, projects, blog posts).

The service is invoked directly by the Backend API Lambda function (not exposed via API Gateway) and uses Amazon Bedrock, OpenAI, Anthropic, or Gemini for LLM inference.

## Architecture

- **Framework**: Strands Agents SDK
- **Runtime**: Python 3.11
- **Deployment**: AWS Lambda via Serverless Framework
- **Region**: ap-southeast-2 (Sydney)
- **LLM Providers**: Amazon Bedrock (default), OpenAI, Anthropic, Gemini
- **Database**: DynamoDB (for tool data access)
- **Secrets**: AWS Secrets Manager (for API keys)

## Prerequisites

Before deploying, ensure you have:

1. **AWS Account** with appropriate permissions
2. **AWS CLI** configured with credentials:
   ```bash
   aws configure
   ```
3. **Node.js** (v18+) and npm installed
4. **Python 3.11** installed
5. **Serverless Framework** installed globally:
   ```bash
   npm install -g serverless
   ```
6. **Docker** (required for packaging Python dependencies)
7. **Backend Service Deployed**: The backend service should be deployed first (see `../my-website-backend/README.md`)

## Setup

### 1. Install Dependencies

```bash
cd agent-service

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Serverless plugins
serverless plugin install -n serverless-python-requirements
```

### 2. Configure AWS Credentials

Ensure your AWS credentials are configured:

```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region: ap-southeast-2
# Default output format: json
```

### 3. Set Up Secrets Manager (Optional)

If using non-Bedrock providers, store API keys in AWS Secrets Manager:

```bash
# For OpenAI (if not using Bedrock)
aws secretsmanager create-secret \
  --name dev/portfolio/openai-api-key \
  --secret-string "your-openai-api-key" \
  --region ap-southeast-2

# For Anthropic (if not using Bedrock)
aws secretsmanager create-secret \
  --name dev/portfolio/anthropic-api-key \
  --secret-string "your-anthropic-api-key" \
  --region ap-southeast-2

# For Gemini (if not using Bedrock)
aws secretsmanager create-secret \
  --name dev/portfolio/gemini-api-key \
  --secret-string "your-gemini-api-key" \
  --region ap-southeast-2
```

**Note**: Amazon Bedrock (default) doesn't require API keys - it uses IAM roles for authentication.

### 4. Ensure DynamoDB Tables Exist

The agent service needs access to DynamoDB tables for tool queries:
- `{stage}-portfolio-blog-posts` (for blog tools)
- Other tables may be needed as content is migrated

These should be created by the backend service deployment.

## Deployment

### Deploy to Development

```bash
# Make sure you're in the agent-service directory
cd agent-service

# Activate virtual environment
source venv/bin/activate

# Deploy to dev stage
serverless deploy --stage dev --verbose
```

### Deploy to Production

```bash
serverless deploy --stage prod --verbose
```

### Deployment Output

After successful deployment, you'll see output like:

```
Service Information
service: agent-service
stage: dev
region: ap-southeast-2
...
functions:
  agent: agent-service-dev-agent
...
```

**Note the function name** - you'll need it for backend configuration: `agent-service-{stage}-agent`

### Update Backend Configuration

After deploying the agent service, update the backend's `AGENT_FUNCTION_NAME` environment variable:

```bash
# Update backend Lambda function configuration
aws lambda update-function-configuration \
  --function-name my-website-backend-dev-api \
  --environment Variables="{AGENT_FUNCTION_NAME=agent-service-dev-agent,STAGE=dev,...}"
```

Or add it to the backend's `serverless.yml`:

```yaml
environment:
  AGENT_FUNCTION_NAME: agent-service-${self:provider.stage}-agent
```

## Configuration

### Environment Variables

The following environment variables are set automatically by Serverless:

- `STAGE`: Deployment stage (dev, prod)
- `CHAT_CONVERSATIONS_TABLE`: DynamoDB table name (for future use)
- `BLOG_POSTS_TABLE`: DynamoDB table name for blog posts
- `ANALYTICS_TABLE`: DynamoDB table name (for future use)
- `PYTHONPATH`: Set to `/var/task` for Lambda

### Model Provider Configuration

The agent service supports multiple LLM providers:

1. **Amazon Bedrock** (default, recommended)
   - No API key required
   - Uses IAM roles for authentication
   - Model: `bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0`

2. **OpenAI**
   - Requires API key in Secrets Manager: `{stage}/portfolio/openai-api-key`
   - Model: `openai/gpt-4o`

3. **Anthropic**
   - Requires API key in Secrets Manager: `{stage}/portfolio/anthropic-api-key`
   - Model: `anthropic/claude-3-5-sonnet-20241022`

4. **Gemini**
   - Requires API key in Secrets Manager: `{stage}/portfolio/gemini-api-key`
   - Model: `gemini/gemini-1.5-pro`

The provider is specified in the request from the backend API.

## Custom Tools

The agent service includes 13 custom tools:

### Profile Tools
- `get_about_me()` - Get profile information
- `get_skills()` - Get technical skills
- `get_education()` - Get education history
- `get_work_experience()` - Get work experience
- `get_experience_details(company_or_role)` - Get specific role details
- `get_contact_info()` - Get contact information
- `get_resume_summary()` - Get comprehensive resume summary

### Blog Tools
- `search_blog_posts(query)` - Search blog posts
- `get_blog_post(slug)` - Get blog post by slug
- `list_recent_blog_posts(limit)` - List recent posts
- `get_blog_posts_by_tag(tag)` - Filter posts by tag

### Project Tools
- `search_projects(query)` - Search projects
- `get_project_details(project_name)` - Get project details
- `list_all_projects()` - List all projects

## Testing

### Test via Backend API

The agent service is invoked by the backend, so test through the backend API:

```bash
# Test chat endpoint (which invokes agent service)
curl -X POST https://abc123.execute-api.ap-southeast-2.amazonaws.com/dev/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session-123",
    "messages": [
      {"role": "user", "content": "What is your background?"}
    ],
    "model_provider": "bedrock"
  }'
```

### Direct Lambda Invocation (Testing)

You can test the agent service directly using AWS CLI:

```bash
aws lambda invoke \
  --function-name agent-service-dev-agent \
  --payload '{
    "session_id": "test-123",
    "messages": [
      {"role": "user", "content": "What are your skills?"}
    ],
    "model_provider": "bedrock"
  }' \
  --region ap-southeast-2 \
  response.json

cat response.json
```

## Monitoring

### View Logs

```bash
# Tail logs in real-time
serverless logs --function agent --stage dev --tail

# View recent logs
serverless logs --function agent --stage dev
```

### CloudWatch Metrics

Monitor your Lambda function in AWS CloudWatch:
- Invocations
- Duration
- Errors
- Throttles
- Memory usage

## Troubleshooting

### Common Issues

1. **Docker not running**: The `serverless-python-requirements` plugin requires Docker for packaging dependencies. Ensure Docker is running.

2. **Permission errors**: Ensure your AWS credentials have permissions for:
   - Lambda
   - DynamoDB
   - Secrets Manager
   - IAM (for role creation)
   - Bedrock (if using Bedrock models)

3. **Bedrock access denied**: If using Bedrock, ensure:
   - Your IAM role has `bedrock:InvokeModel` permission
   - The model is enabled in your AWS account (Bedrock console)

4. **Agent Service not found by backend**: Ensure:
   - Agent service is deployed
   - Backend's `AGENT_FUNCTION_NAME` environment variable matches the deployed function name
   - Both services are in the same AWS region

5. **Import errors**: Ensure all dependencies are in `requirements.txt` and virtual environment is activated.

6. **Strands Agents import error**: Ensure `strands-agents` and `strands-agents-tools` are installed:
   ```bash
   pip install strands-agents strands-agents-tools
   ```

### Debug Mode

Enable verbose logging:

```bash
serverless deploy --stage dev --verbose
```

Check CloudWatch logs for detailed error messages:

```bash
aws logs tail /aws/lambda/agent-service-dev-agent --follow --region ap-southeast-2
```

## Rollback

If you need to rollback to a previous deployment:

```bash
# List deployments
serverless deploy list --stage dev

# Rollback to specific timestamp
serverless rollback --timestamp <timestamp> --stage dev
```

## Cost Estimation

- **Development**: ~$1-3/month
  - Lambda: Free tier (1M requests/month)
  - DynamoDB: ~$0.50 (tool queries)
  - Secrets Manager: $0.40/secret/month
  - Bedrock: Pay-per-use (very low for dev)

- **Production**: ~$10-20/month (10x traffic + Bedrock usage)

**Note**: Bedrock pricing varies by model. Claude 3.5 Sonnet is cost-effective for production use.

## Architecture Notes

### Why Separate Service?

The agent service is separated from the backend to:
1. **Resolve dependency conflicts**: Strands Agents requires `anyio>=4.0`, while FastAPI requires `anyio<4.0`
2. **Independent scaling**: Agent service can scale separately based on AI workload
3. **Easier maintenance**: Update Strands SDK without affecting main API
4. **Cost optimization**: Agent Lambda only runs when AI inference is needed

### Request Flow

```
Frontend → Backend API (FastAPI) → Agent Service (Strands) → LLM Provider
                ↓                           ↓
          DynamoDB (chat)            DynamoDB (content)
```

## Next Steps

1. Deploy the backend service first (see `../my-website-backend/README.md`)
2. Deploy this agent service
3. Update backend's `AGENT_FUNCTION_NAME` environment variable
4. Test end-to-end chat functionality
5. Monitor CloudWatch logs and metrics

## Support

For issues or questions, refer to:
- [Serverless Framework Docs](https://www.serverless.com/framework/docs)
- [Strands Agents Documentation](https://github.com/aws/strands-agents)
- [AWS Lambda Docs](https://docs.aws.amazon.com/lambda/)
- [Amazon Bedrock Docs](https://docs.aws.amazon.com/bedrock/)

