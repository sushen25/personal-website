# My Website Backend

FastAPI backend service for the portfolio website, deployed as a serverless Lambda function on AWS.

## Overview

This service provides the main API Gateway endpoint for the portfolio website, handling:
- Chat API endpoints (`/api/chat`)
- Blog API endpoints (future)
- Analytics endpoints (future)
- Health check endpoint (`/health`)

The backend orchestrates chat requests by invoking the separate Agent Service Lambda function and manages conversation persistence in DynamoDB.

## Architecture

- **Framework**: FastAPI with Mangum (ASGI adapter for Lambda)
- **Runtime**: Python 3.11
- **Deployment**: AWS Lambda via Serverless Framework
- **Region**: ap-southeast-2 (Sydney)
- **API Gateway**: HTTP API (v2)
- **Database**: DynamoDB (chat conversations, blog posts, analytics)
- **Secrets**: AWS Secrets Manager

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

## Setup

### 1. Install Dependencies

```bash
cd my-website-backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
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

## Deployment

### Deploy to Development

```bash
# Make sure you're in the my-website-backend directory
cd my-website-backend

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
service: my-website-backend
stage: dev
region: ap-southeast-2
...
endpoints:
  ANY - https://abc123.execute-api.ap-southeast-2.amazonaws.com/dev/{proxy+}
  ANY - https://abc123.execute-api.ap-southeast-2.amazonaws.com/dev
...
```

**Save the API Gateway URL** - you'll need it for frontend configuration.

### Update Environment Variables

After deployment, update your frontend `.env.local`:

```env
NEXT_PUBLIC_API_URL=https://abc123.execute-api.ap-southeast-2.amazonaws.com/dev
NEXT_PUBLIC_CHAT_API_URL=https://abc123.execute-api.ap-southeast-2.amazonaws.com/dev/api/chat
```

## Configuration

### Environment Variables

The following environment variables are set automatically by Serverless:

- `STAGE`: Deployment stage (dev, prod)
- `CHAT_CONVERSATIONS_TABLE`: DynamoDB table name for chat conversations
- `BLOG_POSTS_TABLE`: DynamoDB table name for blog posts
- `ANALYTICS_TABLE`: DynamoDB table name for analytics
- `PYTHONPATH`: Set to `/var/task` for Lambda

### Agent Service Configuration

The backend needs to know the Agent Service Lambda function name. Set it as an environment variable:

```bash
# In serverless.yml, add to environment section:
AGENT_FUNCTION_NAME: agent-service-${self:provider.stage}-agent
```

Or set it manually after deployment:

```bash
aws lambda update-function-configuration \
  --function-name my-website-backend-dev-api \
  --environment Variables="{AGENT_FUNCTION_NAME=agent-service-dev-agent}"
```

## Testing

### Local Testing with Serverless Offline

```bash
# Install serverless-offline plugin
serverless plugin install -n serverless-offline

# Start local server
serverless offline start
```

The API will be available at `http://localhost:3000`

### Test Endpoints

```bash
# Health check
curl https://abc123.execute-api.ap-southeast-2.amazonaws.com/dev/health

# Chat endpoint
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

## Monitoring

### View Logs

```bash
# Tail logs in real-time
serverless logs --function api --stage dev --tail

# View recent logs
serverless logs --function api --stage dev
```

### CloudWatch Metrics

Monitor your Lambda function in AWS CloudWatch:
- Invocations
- Duration
- Errors
- Throttles

## Troubleshooting

### Common Issues

1. **Docker not running**: The `serverless-python-requirements` plugin requires Docker for packaging dependencies. Ensure Docker is running.

2. **Permission errors**: Ensure your AWS credentials have permissions for:
   - Lambda
   - API Gateway
   - DynamoDB
   - Secrets Manager
   - IAM (for role creation)

3. **Agent Service not found**: Ensure the Agent Service is deployed first and the function name matches in `AGENT_FUNCTION_NAME`.

4. **DynamoDB table not found**: Create the required DynamoDB tables before deploying or uncomment the CloudFormation resources in `serverless.yml`.

5. **Import errors**: Ensure all dependencies are in `requirements.txt` and virtual environment is activated.

### Debug Mode

Enable verbose logging:

```bash
serverless deploy --stage dev --verbose
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

- **Development**: ~$3-5/month
  - Lambda: Free tier (1M requests/month)
  - API Gateway: Free tier (1M requests/month)
  - DynamoDB: ~$1-2 (on-demand, low traffic)
  - Secrets Manager: $0.40/secret/month

- **Production**: ~$20-30/month (10x traffic)

## Next Steps

1. Deploy the Agent Service (see `../agent-service/README.md`)
2. Update frontend environment variables
3. Test end-to-end chat functionality
4. Monitor CloudWatch logs and metrics

## Support

For issues or questions, refer to:
- [Serverless Framework Docs](https://www.serverless.com/framework/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [AWS Lambda Docs](https://docs.aws.amazon.com/lambda/)

