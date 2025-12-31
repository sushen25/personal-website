#!/bin/bash

# Script to set up API key in AWS Secrets Manager
# Usage: ./setup-api-key.sh [stage] [region]

set -e

STAGE=${1:-dev}
REGION=${2:-ap-southeast-2}
SECRET_NAME="${STAGE}/portfolio/portfolio-api-key"

echo "Setting up API key for stage: $STAGE in region: $REGION"

# Generate a secure random API key (64 characters)
API_KEY=$(openssl rand -hex 32)

echo "Generated API key: $API_KEY"
echo ""
echo "Creating secret in AWS Secrets Manager..."

# Check if secret already exists
if aws secretsmanager describe-secret --secret-id "$SECRET_NAME" --region "$REGION" 2>/dev/null; then
    echo "Secret already exists. Updating..."
    aws secretsmanager update-secret \
        --secret-id "$SECRET_NAME" \
        --secret-string "$API_KEY" \
        --region "$REGION"
    echo "Secret updated successfully!"
else
    echo "Creating new secret..."
    aws secretsmanager create-secret \
        --name "$SECRET_NAME" \
        --description "API key for portfolio website chat authentication" \
        --secret-string "$API_KEY" \
        --region "$REGION"
    echo "Secret created successfully!"
fi

echo ""
echo "=========================================="
echo "API Key Setup Complete!"
echo "=========================================="
echo ""
echo "Secret Name: $SECRET_NAME"
echo "API Key: $API_KEY"
echo ""
echo "IMPORTANT: Save this API key securely!"
echo "You'll need to add it to your frontend environment variables:"
echo ""
echo "In my-website-frontend/.env.local:"
echo "NEXT_PUBLIC_API_KEY=$API_KEY"
echo ""
echo "In my-website-frontend/.env.production:"
echo "NEXT_PUBLIC_API_KEY=$API_KEY"
echo ""
echo "=========================================="
