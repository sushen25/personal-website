# Portfolio Website Deployment Guide

Complete guide for deploying the portfolio website with all three services.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Portfolio Website                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Frontend (Next.js)  →  Backend (FastAPI)  →  Agent Service │
│       S3 + CF            Lambda + APIGW        AgentCore     │
│                                                               │
│  Shared: portfolio-common (Python package)                   │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

### Required Tools
- **AWS CLI** configured with credentials
- **Node.js** 18+ and npm
- **Python** 3.11+ (3.12 for agent-service)
- **Docker** (for packaging Python dependencies)
- **Serverless Framework**: `npm install -g serverless`
- **AgentCore CLI**: `pip install bedrock-agentcore-starter-toolkit`

### AWS Permissions Required
- Lambda (create/update functions, layers)
- API Gateway (create/manage APIs)
- DynamoDB (create/manage tables)
- S3 (create buckets, upload files)
- IAM (create roles and policies)
- CloudFormation (stack management)
- Bedrock AgentCore (deploy agents)
- Secrets Manager (store API keys)

### Initial Setup

```bash
# Configure AWS credentials
aws configure

# Verify AWS access
aws sts get-caller-identity

# Install global tools
npm install -g serverless
pip install bedrock-agentcore-starter-toolkit
```

## Deployment Order

**IMPORTANT**: Deploy in this exact order due to dependencies:

1. **portfolio-common** (build package)
2. **agent-service** (AgentCore Runtime)
3. **my-website-backend** (Serverless Framework)
4. **my-website-frontend** (S3 + CloudFront)

## 1. Build portfolio-common Package

The `portfolio-common` package contains shared code used by both backend and agent-service.

### Why Build as Wheel?

For agentcore deployment, we cannot use editable installs (`-e ../portfolio-common`). We need to build a proper wheel package.

### Build Steps

```bash
cd portfolio-common

# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Install build tool
pip install --upgrade build

# Build wheel
python3 -m build

# Verify wheel created
ls -lh dist/
# Should see: portfolio_common-0.1.0-py3-none-any.whl
```

**Output**: `dist/portfolio_common-0.1.0-py3-none-any.whl`

## 2. Deploy Agent Service (AgentCore Runtime)

The agent service powers the AI chatbot using Strands Agents framework and Bedrock AgentCore.

### Configuration

First, configure the agent (only needed once):

```bash
cd agent-service

# Configure agentcore
agentcore configure -e src/main.py
```

This will prompt for:
- **AWS Execution Role**: Choose "auto-create" or provide existing role ARN
- **ECR Repository**: Choose "auto-create" for container registry
- **Requirements file**: Confirm `requirements.txt` path
- **Memory features**: Enable STM (short-term memory) if desired
- **Region**: `ap-southeast-2` (Sydney)

This creates `.bedrock_agentcore.yaml` with your configuration.

### Handle portfolio-common Dependency

AgentCore cannot deploy with editable installs. We need to modify requirements.txt temporarily:

```bash
# Backup original
cp requirements.txt requirements.txt.backup

# Create deployment version
cat > requirements.txt.deploy <<EOF
strands-agents==1.19.0
strands-agents-builder==0.1.10
strands-agents-tools==0.2.17
bedrock-agentcore==1.1.1
boto3>=1.34.0
python-dotenv==1.0.0

# Use wheel instead of editable install
../portfolio-common/dist/portfolio_common-0.1.0-py3-none-any.whl
EOF

# Use deployment version
mv requirements.txt requirements.txt.backup2
mv requirements.txt.deploy requirements.txt
```

### Deploy

```bash
# Deploy to AgentCore Runtime
agentcore deploy --region ap-southeast-2

# Check deployment status
agentcore status

# Test the agent
agentcore invoke '{"prompt": "What are your skills?", "session_id": "test-123"}'
```

### Get Agent ARN

```bash
# Get agent ARN for backend configuration
agentcore status

# Example output:
# Agent ARN: arn:aws:bedrock-agentcore:ap-southeast-2:123456789:agent/abc-123
```

**Save this ARN** - you'll need it for backend deployment.

### Restore Original Requirements

```bash
# After successful deployment, restore original
mv requirements.txt.backup2 requirements.txt
```

### Environment Variables

The agent needs access to DynamoDB tables. These are auto-configured:
- `BLOG_POSTS_TABLE`: `dev-portfolio-blog-posts`
- `CHAT_CONVERSATIONS_TABLE`: `dev-portfolio-chat-conversations`

For API keys (if using non-Bedrock providers), store in AWS Secrets Manager:

```bash
# Example: Store Anthropic API key
aws secretsmanager create-secret \
  --name dev/portfolio/anthropic-api-key \
  --secret-string "your-api-key-here" \
  --region ap-southeast-2
```

## 3. Deploy Backend (Serverless Framework)

The backend is a FastAPI application deployed as AWS Lambda with API Gateway.

### Verify portfolio-common Dependency

Check that `requirements.txt` includes portfolio-common:

```bash
cd my-website-backend
grep "portfolio-common" requirements.txt
# Should show: -e ../portfolio-common
```

✅ Already configured!

### Set Environment Variables

Create or update `.env` file:

```bash
cat > .env <<EOF
AWS_REGION=ap-southeast-2
AWS_PROFILE=default
STAGE=dev
CHAT_CONVERSATIONS_TABLE=dev-portfolio-chat-conversations
BLOG_POSTS_TABLE=dev-portfolio-blog-posts
ANALYTICS_TABLE=dev-portfolio-analytics

# Agent Service ARN (from step 2)
AGENT_SERVICE_URL=arn:aws:bedrock-agentcore:ap-southeast-2:123456789:agent/your-agent-id
EOF
```

### Deploy

```bash
cd my-website-backend

# Install Node dependencies (serverless plugins)
npm install

# Create Python virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies (including portfolio-common)
pip install -r requirements.txt

# Deploy to AWS
serverless deploy --stage dev --region ap-southeast-2 --verbose
```

### Get Deployment Info

After deployment, note these URLs:

```bash
serverless info --stage dev

# Example output:
# endpoints:
#   ANY - https://abc123.execute-api.ap-southeast-2.amazonaws.com/dev/{proxy+}
#   ANY - https://abc123.execute-api.ap-southeast-2.amazonaws.com/dev
#
# ApiStreamFunctionUrl:
#   https://xyz789.lambda-url.ap-southeast-2.on.aws/
```

**Save these URLs** - you'll need them for frontend configuration.

### Test Backend

```bash
# Test health endpoint
curl https://abc123.execute-api.ap-southeast-2.amazonaws.com/dev/health

# Test chat endpoint
curl -X POST https://abc123.execute-api.ap-southeast-2.amazonaws.com/dev/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-session",
    "messages": [{"role": "user", "content": "Hello"}],
    "model_provider": "bedrock"
  }'
```

## 4. Deploy Frontend (S3 + CloudFront)

The frontend is a Next.js application deployed as a static site to S3.

### Configure Environment Variables

Create production environment file:

```bash
cd my-website-frontend

cat > .env.production <<EOF
# Backend API URL (from step 3)
NEXT_PUBLIC_API_URL=https://abc123.execute-api.ap-southeast-2.amazonaws.com/dev
NEXT_PUBLIC_CHAT_API_URL=https://abc123.execute-api.ap-southeast-2.amazonaws.com/dev/api/chat
EOF
```

### Build Frontend

```bash
# Install dependencies
npm install

# Build for production
npm run build

# Verify output directory created
ls -la out/
```

### Verify serverless.yml Configuration

Check S3 bucket configuration:

```bash
cat serverless.yml

# Should show:
# custom:
#   client:
#     bucketName: sushensatturu-com-frontend
#     distributionFolder: out
```

### Deploy to S3

```bash
# Deploy using serverless-finch plugin
npx serverless client deploy --stage dev --region ap-southeast-2 --no-confirm
```

### Get Frontend URL

```bash
# S3 website URL
echo "http://sushensatturu-com-frontend.s3-website-ap-southeast-2.amazonaws.com"

# Or check S3 bucket properties in AWS Console
aws s3 website s3://sushensatturu-com-frontend
```

## Automated Deployment

Use the provided deployment script for automated deployment:

```bash
# From repository root
./deploy.sh

# Or with custom stage/region
STAGE=prod AWS_REGION=us-east-1 ./deploy.sh
```

The script will:
1. ✅ Build portfolio-common wheel
2. ✅ Deploy agent-service to AgentCore
3. ✅ Deploy backend to Lambda
4. ✅ Build and deploy frontend to S3
5. ✅ Display deployment summary with all URLs

## Post-Deployment Testing

### Test Full Flow

```bash
# 1. Test backend health
curl https://your-api-url/dev/health

# 2. Test agent via backend
curl -X POST https://your-api-url/dev/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-123",
    "messages": [{"role": "user", "content": "What are your skills?"}],
    "model_provider": "bedrock"
  }'

# 3. Visit frontend
open http://sushensatturu-com-frontend.s3-website-ap-southeast-2.amazonaws.com
```

### Monitor Logs

```bash
# Agent logs
agentcore logs --follow

# Backend logs
cd my-website-backend
serverless logs --function api --stage dev --tail

# Backend streaming logs
serverless logs --function apiStream --stage dev --tail
```

## Updating Deployments

### Update Agent Service

```bash
cd agent-service

# Make code changes, then redeploy
agentcore deploy
```

### Update Backend

```bash
cd my-website-backend

# Make code changes, then redeploy
serverless deploy --stage dev

# Or deploy single function
serverless deploy function --function api --stage dev
```

### Update Frontend

```bash
cd my-website-frontend

# Update environment variables if needed
# Make code changes, rebuild and redeploy
npm run build
npx serverless client deploy --no-confirm
```

## Troubleshooting

### Agent Service Issues

**Problem**: `agentcore deploy` fails with dependency errors

**Solution**: Ensure portfolio-common wheel is built and requirements.txt references the wheel (not editable install)

```bash
cd portfolio-common
python3 -m build
cd ../agent-service
# Update requirements.txt to use ../portfolio-common/dist/portfolio_common-0.1.0-py3-none-any.whl
```

**Problem**: Agent ARN not found

**Solution**: Check agent status
```bash
agentcore status
# Copy the ARN and update backend .env
```

### Backend Issues

**Problem**: Lambda can't find portfolio-common modules

**Solution**: Reinstall dependencies in virtual environment
```bash
cd my-website-backend
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

**Problem**: CORS errors when calling from frontend

**Solution**: Verify CORS configuration in serverless.yml (already configured with `origin: '*'`)

### Frontend Issues

**Problem**: API calls fail with 404

**Solution**: Check environment variables
```bash
# Verify .env.production has correct API URLs
cat .env.production
# Rebuild
npm run build
```

**Problem**: Static export fails

**Solution**: Ensure Next.js is configured for static export
```bash
# Check next.config.ts has:
# output: 'export'
```

## Cost Estimation

### Development Environment (dev stage)
- **Agent Service**: ~$2-5/month
  - AgentCore runtime (minimal usage)
  - Bedrock API calls (pay-per-use)
- **Backend**: ~$1-3/month
  - Lambda (Free tier: 1M requests)
  - API Gateway (Free tier: 1M requests)
  - DynamoDB (Free tier: 25GB, 25 WCU/RCU)
- **Frontend**: ~$1-2/month
  - S3 hosting (~$0.023/GB)
  - Data transfer (~$0.09/GB)

**Total**: ~$5-10/month for development

### Production Environment (prod stage)
- **Agent Service**: ~$20-50/month (depends on usage)
- **Backend**: ~$10-20/month
- **Frontend**: ~$5-10/month

**Total**: ~$35-80/month for production

## Rollback Procedures

### Rollback Agent

```bash
agentcore deploy --rollback
```

### Rollback Backend

```bash
cd my-website-backend
serverless rollback --timestamp <timestamp> --stage dev
```

### Rollback Frontend

Redeploy previous build:
```bash
cd my-website-frontend
git checkout <previous-commit>
npm run build
npx serverless client deploy --no-confirm
git checkout main
```

## CI/CD Integration

For automated deployments, add to GitHub Actions:

```yaml
# .github/workflows/deploy.yml
name: Deploy Portfolio

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ap-southeast-2
      - name: Deploy
        run: ./deploy.sh
```

## Support

For issues:
1. Check CloudWatch logs
2. Review agent logs with `agentcore logs`
3. Verify all environment variables are set
4. Ensure portfolio-common is properly built and installed

## Summary

✅ **portfolio-common**: Build wheel package
✅ **agent-service**: Deploy to AgentCore Runtime
✅ **backend**: Deploy to Lambda + API Gateway
✅ **frontend**: Deploy to S3 + CloudFront

All services are now deployed and ready to use!
