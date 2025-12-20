#!/bin/bash

# Portfolio Website Deployment Script
# Deploys agent-service (agentcore), backend (serverless), and frontend (S3)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
STAGE=${STAGE:-dev}
AWS_REGION=${AWS_REGION:-ap-southeast-2}
REPO_ROOT=$(pwd)

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}Portfolio Website Deployment${NC}"
echo -e "${GREEN}Stage: $STAGE | Region: $AWS_REGION${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""

# Function to print step headers
print_step() {
    echo -e "\n${YELLOW}>>> $1${NC}\n"
}

# Function to print success
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print error
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

#############################################
# STEP 1: Build portfolio-common package
#############################################
print_step "STEP 1: Building portfolio-common package"

cd "$REPO_ROOT/portfolio-common"

# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build wheel package
python3 -m pip install --upgrade build
python3 -m build

# Verify wheel was created
if [ ! -f "dist/portfolio_common-0.1.0-py3-none-any.whl" ]; then
    print_error "Failed to build portfolio-common wheel"
    exit 1
fi

print_success "portfolio-common wheel built successfully"

#############################################
# STEP 2: Deploy Agent Service (AgentCore)
#############################################
print_step "STEP 2: Deploying Agent Service (AgentCore Runtime)"

cd "$REPO_ROOT/agent-service"

# Check if agentcore CLI is installed
if ! command -v agentcore &> /dev/null; then
    print_error "agentcore CLI not found. Installing..."
    pip install bedrock-agentcore-starter-toolkit
fi

# Create temporary requirements.txt for deployment (without editable install)
cp requirements.txt requirements.txt.backup
cat > requirements.txt.deploy <<EOF
# Strands Agents Framework
strands-agents==1.19.0
strands-agents-builder==0.1.10
strands-agents-tools==0.2.17

# Bedrock agent code
bedrock-agentcore==1.1.1

# AWS SDK (for DynamoDB access in tools)
boto3>=1.34.0

# Environment variables
python-dotenv==1.0.0

# Shared portfolio package (from wheel)
../portfolio-common/dist/portfolio_common-0.1.0-py3-none-any.whl
EOF

# Backup original and use deployment version
mv requirements.txt requirements.txt.backup
mv requirements.txt.deploy requirements.txt

# Check if agent is already configured
if [ ! -f ".bedrock_agentcore.yaml" ]; then
    print_error "Agent not configured. Please run: agentcore configure -e src/main.py"
    mv requirements.txt.backup requirements.txt
    exit 1
fi

# Deploy agent
echo "Deploying agent to AgentCore Runtime..."
agentcore deploy

# Get agent ARN/ID from deployment
AGENT_ARN=$(agentcore status | grep -oP 'arn:aws:bedrock-agentcore:[^"]+' || echo "")

if [ -z "$AGENT_ARN" ]; then
    print_error "Failed to get agent ARN. Check agentcore status manually."
else
    print_success "Agent deployed successfully: $AGENT_ARN"

    # Save agent ARN for backend configuration
    echo "$AGENT_ARN" > "$REPO_ROOT/.agent_arn"
fi

# Restore original requirements.txt
mv requirements.txt.backup requirements.txt

print_success "Agent service deployment complete"

#############################################
# STEP 3: Deploy Backend (Serverless)
#############################################
print_step "STEP 3: Deploying Backend (Serverless Framework)"

cd "$REPO_ROOT/my-website-backend"

# Install serverless plugins if needed
if [ ! -d "node_modules" ]; then
    npm install
fi

# Activate Python virtual environment
if [ ! -d "venv" ]; then
    python3.11 -m venv venv
fi
source venv/bin/activate

# Install Python dependencies (includes portfolio-common)
pip install -r requirements.txt

# Set environment variables for deployment
export AGENT_SERVICE_URL="${AGENT_ARN}"  # Use agent ARN as the service URL

# Deploy backend
echo "Deploying backend to AWS Lambda..."
serverless deploy --stage "$STAGE" --region "$AWS_REGION" --verbose

# Get API Gateway URL
API_URL=$(serverless info --stage "$STAGE" --verbose 2>/dev/null | grep -oP 'https://[^/]+\.execute-api\.[^/]+/[^/]+' | head -1 || echo "")
STREAM_URL=$(serverless info --stage "$STAGE" --verbose 2>/dev/null | grep -oP 'https://[^.]+\.lambda-url\.[^/]+' | head -1 || echo "")

if [ -z "$API_URL" ]; then
    print_error "Failed to get API Gateway URL. Check serverless info manually."
else
    print_success "Backend deployed successfully"
    echo "API URL: $API_URL"
    echo "Stream URL: $STREAM_URL"

    # Save URLs for frontend configuration
    echo "$API_URL" > "$REPO_ROOT/.backend_api_url"
    echo "$STREAM_URL" > "$REPO_ROOT/.backend_stream_url"
fi

deactivate

#############################################
# STEP 4: Build Frontend
#############################################
print_step "STEP 4: Building Frontend"

cd "$REPO_ROOT/my-website-frontend"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    npm install
fi

# Create production environment file
if [ -n "$API_URL" ]; then
    cat > .env.production <<EOF
# Production Environment Variables
NEXT_PUBLIC_API_URL=$API_URL
NEXT_PUBLIC_CHAT_API_URL=$API_URL/api/chat
EOF
    print_success "Environment variables configured"
else
    print_error "No API URL found. Please update .env.production manually"
fi

# Build frontend
echo "Building Next.js for production..."
npm run build

# Export static site
if [ ! -d "out" ]; then
    print_error "Build failed - 'out' directory not created"
    exit 1
fi

print_success "Frontend built successfully"

#############################################
# STEP 5: Deploy Frontend (S3 + CloudFront)
#############################################
print_step "STEP 5: Deploying Frontend to S3"

# Deploy using serverless-finch
echo "Deploying frontend to S3..."
npx serverless client deploy --stage "$STAGE" --region "$AWS_REGION" --no-confirm

# Get CloudFront URL (if configured)
S3_BUCKET="sushensatturu-com-frontend"
print_success "Frontend deployed to S3"
echo "S3 Bucket: $S3_BUCKET"

#############################################
# DEPLOYMENT SUMMARY
#############################################
print_step "DEPLOYMENT SUMMARY"

echo -e "${GREEN}All services deployed successfully!${NC}"
echo ""
echo "Agent Service:"
echo "  ARN: ${AGENT_ARN:-'Check with: agentcore status'}"
echo ""
echo "Backend API:"
echo "  URL: ${API_URL:-'Check with: serverless info --stage dev'}"
echo "  Stream URL: ${STREAM_URL:-'Check serverless info'}"
echo ""
echo "Frontend:"
echo "  S3 Bucket: $S3_BUCKET"
echo "  URL: http://$S3_BUCKET.s3-website-$AWS_REGION.amazonaws.com"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Test the backend API: curl $API_URL/health"
echo "2. Test the agent: agentcore invoke '{\"prompt\":\"Hello\"}'"
echo "3. Visit your frontend URL to test end-to-end"
echo ""
