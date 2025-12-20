# Deployment Checklist

Quick reference for deploying the portfolio website.

## Pre-Deployment Checks

### ✅ Tools Installed
- [ ] AWS CLI configured (`aws configure`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] Python 3.11+ installed (`python3 --version`)
- [ ] Docker running (`docker ps`)
- [ ] Serverless Framework installed (`serverless --version`)
- [ ] AgentCore CLI installed (`agentcore --version`)

### ✅ AWS Credentials
- [ ] AWS credentials configured (`aws sts get-caller-identity`)
- [ ] Correct AWS profile set (`echo $AWS_PROFILE`)
- [ ] Permissions verified (Lambda, API Gateway, DynamoDB, S3, Bedrock)

### ✅ Environment Variables

**Agent Service** (`agent-service/.env`):
```bash
AWS_REGION=ap-southeast-2
STAGE=dev
BLOG_POSTS_TABLE=dev-portfolio-blog-posts
CHAT_CONVERSATIONS_TABLE=dev-portfolio-chat-conversations
```

**Backend** (`my-website-backend/.env`):
```bash
AWS_REGION=ap-southeast-2
STAGE=dev
CHAT_CONVERSATIONS_TABLE=dev-portfolio-chat-conversations
BLOG_POSTS_TABLE=dev-portfolio-blog-posts
ANALYTICS_TABLE=dev-portfolio-analytics
AGENT_SERVICE_URL=<agent-arn-from-deployment>
```

**Frontend** (`my-website-frontend/.env.production`):
```bash
NEXT_PUBLIC_API_URL=<backend-api-url>
NEXT_PUBLIC_CHAT_API_URL=<backend-api-url>/api/chat
```

## Deployment Steps

### Step 1: Build portfolio-common (5 minutes)

```bash
cd portfolio-common
rm -rf dist/ build/ *.egg-info
python3 -m build
ls dist/  # Should see: portfolio_common-0.1.0-py3-none-any.whl
```

- [ ] Wheel file created in `dist/`
- [ ] No build errors

### Step 2: Configure Agent Service (First time only, 10 minutes)

```bash
cd agent-service
agentcore configure -e src/main.py
```

**Configuration prompts:**
- [ ] AWS Execution Role: Auto-create ✅
- [ ] ECR Repository: Auto-create ✅
- [ ] Region: `ap-southeast-2` ✅
- [ ] Requirements file: Confirmed ✅
- [ ] `.bedrock_agentcore.yaml` created ✅

### Step 3: Deploy Agent Service (15 minutes)

```bash
cd agent-service

# Modify requirements.txt for deployment
cp requirements.txt requirements.txt.backup
# Edit requirements.txt: Replace "-e ../portfolio-common" with:
# "../portfolio-common/dist/portfolio_common-0.1.0-py3-none-any.whl"

agentcore deploy --region ap-southeast-2
agentcore status  # Get agent ARN

# Restore original
mv requirements.txt.backup requirements.txt
```

- [ ] Agent deployed successfully
- [ ] Agent ARN obtained: `_______________________________`
- [ ] Test passed: `agentcore invoke '{"prompt":"Hello"}'`

### Step 4: Deploy Backend (10 minutes)

```bash
cd my-website-backend

# Update .env with agent ARN
# AGENT_SERVICE_URL=<agent-arn-from-step-3>

npm install
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

serverless deploy --stage dev --region ap-southeast-2 --verbose
serverless info --stage dev
```

- [ ] Backend deployed successfully
- [ ] API Gateway URL: `_______________________________`
- [ ] Stream Function URL: `_______________________________`
- [ ] Test passed: `curl <api-url>/health`

### Step 5: Build & Deploy Frontend (10 minutes)

```bash
cd my-website-frontend

# Update .env.production with backend URLs
# NEXT_PUBLIC_API_URL=<backend-url>
# NEXT_PUBLIC_CHAT_API_URL=<backend-url>/api/chat

npm install
npm run build

npx serverless client deploy --stage dev --region ap-southeast-2 --no-confirm
```

- [ ] Frontend built successfully (`out/` directory created)
- [ ] Deployed to S3
- [ ] S3 URL: `http://sushensatturu-com-frontend.s3-website-ap-southeast-2.amazonaws.com`
- [ ] Frontend loads in browser

## Post-Deployment Verification

### Agent Service
```bash
agentcore invoke '{"prompt": "What are your skills?", "session_id": "test"}'
```
- [ ] Returns valid response
- [ ] No errors in logs: `agentcore logs --follow`

### Backend API
```bash
# Health check
curl https://<api-url>/dev/health

# Chat endpoint
curl -X POST https://<api-url>/dev/api/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test","messages":[{"role":"user","content":"Hello"}],"model_provider":"bedrock"}'
```
- [ ] Health check returns 200 OK
- [ ] Chat returns valid response
- [ ] No errors in logs: `serverless logs --function api --tail`

### Frontend
- [ ] Visit S3 URL in browser
- [ ] Homepage loads correctly
- [ ] Chat interface visible
- [ ] Can send a test message
- [ ] Response appears in chat

## Automated Deployment (Alternative)

Instead of manual steps, use:

```bash
./deploy.sh
```

- [ ] All services deployed successfully
- [ ] Deployment summary displayed
- [ ] All URLs noted

## Troubleshooting Quick Fixes

### Agent deployment fails
```bash
# Check Docker is running
docker ps

# Check requirements.txt uses wheel (not -e ../portfolio-common)
cat agent-service/requirements.txt

# Rebuild portfolio-common
cd portfolio-common && python3 -m build
```

### Backend can't find portfolio-common
```bash
cd my-website-backend
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
serverless deploy --stage dev
```

### Frontend shows API errors
```bash
# Check .env.production
cat my-website-frontend/.env.production

# Rebuild
cd my-website-frontend
npm run build
npx serverless client deploy --no-confirm
```

## URLs to Save

After deployment, record these URLs:

| Service | URL | Notes |
|---------|-----|-------|
| Agent ARN | `arn:aws:bedrock-agentcore:ap-southeast-2:...` | For backend config |
| Backend API | `https://...execute-api.ap-southeast-2.amazonaws.com/dev` | For frontend config |
| Stream URL | `https://...lambda-url.ap-southeast-2.on.aws/` | For streaming chat |
| Frontend | `http://sushensatturu-com-frontend.s3-website-ap-southeast-2.amazonaws.com` | Public URL |

## Monitoring

### View Logs
```bash
# Agent
agentcore logs --follow

# Backend
cd my-website-backend
serverless logs --function api --tail
serverless logs --function apiStream --tail

# CloudWatch (alternative)
aws logs tail /aws/lambda/my-website-backend-dev-api --follow
```

### Check Status
```bash
# Agent
agentcore status

# Backend
cd my-website-backend
serverless info --stage dev

# Frontend (check S3 bucket)
aws s3 ls s3://sushensatturu-com-frontend/
```

## Rollback Plan

If something goes wrong:

### Agent
```bash
agentcore deploy --rollback
```

### Backend
```bash
cd my-website-backend
serverless rollback --timestamp <previous-timestamp> --stage dev
```

### Frontend
```bash
cd my-website-frontend
git checkout <previous-commit>
npm run build
npx serverless client deploy --no-confirm
```

## Next Steps After Deployment

1. [ ] Set up custom domain (Route53 + CloudFront)
2. [ ] Configure CloudFront for frontend (HTTPS + caching)
3. [ ] Set up monitoring alerts (CloudWatch Alarms)
4. [ ] Enable backup for DynamoDB tables
5. [ ] Set up CI/CD pipeline (GitHub Actions)
6. [ ] Configure WAF rules for API Gateway
7. [ ] Enable AWS Cost Explorer alerts

## Support

- **Documentation**: See `DEPLOYMENT_GUIDE.md` for detailed steps
- **Logs**: Check CloudWatch Logs in AWS Console
- **Issues**: Review error messages in deployment output
- **Agent Issues**: Run `agentcore logs --follow`
- **Backend Issues**: Run `serverless logs --tail`

---

**Estimated Total Deployment Time**: 45-60 minutes (first time)
**Estimated Update Time**: 5-10 minutes per service
