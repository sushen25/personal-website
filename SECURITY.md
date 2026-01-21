# Security Documentation

## Table of Contents
1. [Overview](#overview)
2. [Current Security Posture](#current-security-posture)
3. [Known Vulnerabilities](#known-vulnerabilities)
4. [DDoS Protection](#ddos-protection)
5. [Implementation Guides](#implementation-guides)
6. [Security Best Practices](#security-best-practices)
7. [Monitoring and Alerts](#monitoring-and-alerts)
8. [Cost Considerations](#cost-considerations)

---

## Overview

This document provides a comprehensive security assessment of the portfolio website and outlines recommendations for protecting against common attack vectors, including DDoS attacks, API abuse, and other web vulnerabilities.

### Architecture
- **Frontend**: Next.js (static export) on S3 + CloudFront
- **Backend**: FastAPI on AWS Lambda + API Gateway
- **Agent Service**: AWS Bedrock Agent Core Runtime
- **Database**: DynamoDB
- **Region**: ap-southeast-2 (Sydney)

---

## Current Security Posture

### Strengths

#### 1. Secrets Management
- AWS Secrets Manager integration for API keys
- Thread-safe caching with 5-minute TTL
- No hardcoded secrets in codebase
- Secrets stored with pattern: `${stage}/portfolio/{provider}-api-key`

#### 2. Input Validation
- Pydantic models enforce type validation on all API requests
- FastAPI automatic validation for query parameters
- Request validation middleware catches malformed data
- Frontend uses DOMPurify for HTML sanitization (XSS protection)

#### 3. Infrastructure Security
- IAM roles follow least-privilege principle for DynamoDB and Secrets Manager
- DynamoDB encryption at rest (AWS-managed keys)
- TTL enabled on chat conversations for automatic data expiration
- CORS properly configured for production domain (`https://sushensatturu.com`)
- Environment variables excluded from version control

#### 4. Error Handling
- Centralized error handling middleware
- No sensitive data exposed in error responses
- Detailed logging for debugging without information leakage
- Proper HTTP status codes

#### 5. AWS Default Protections
- AWS Shield Standard (free, automatic DDoS protection)
- CloudFront DDoS protection for static frontend
- API Gateway default throttling (10,000 req/sec per account)

---

## Known Vulnerabilities

### Critical (Fix Immediately)

#### 1. No Authentication/Authorization
**Severity**: CRITICAL
**Impact**: Anyone can access and use all API endpoints

**Affected Endpoints**:
- `/api/chat/*` - Open to public, incurs Bedrock API costs
- `/api/blog/*` - No access controls on read operations
- Blog write operations commented out but would be unprotected

**Files**:
- `my-website-backend/src/main.py`
- `my-website-backend/src/handlers/chat.py`
- `my-website-backend/src/handlers/blog.py`

**Risk**:
- Financial impact: Unlimited Bedrock API usage
- Data integrity: Blog content could be manipulated if write endpoints enabled

#### 2. No Rate Limiting
**Severity**: CRITICAL
**Impact**: API abuse and cost attacks

**Issues**:
- No application-level rate limiting
- No throttling configuration in API Gateway beyond defaults
- No per-IP or session-based limits
- Chat endpoint vulnerable to expensive API call abuse

**Risk**:
- Cost attack: Malicious actor could generate large AWS bills
- Service degradation: Legitimate users affected by abuse

#### 3. Missing Security Headers
**Severity**: HIGH
**Impact**: Vulnerable to XSS, clickjacking, and other browser-based attacks

**Missing Headers**:
- `Content-Security-Policy` (CSP)
- `Strict-Transport-Security` (HSTS)
- `X-Frame-Options`
- `X-Content-Type-Options`
- `X-XSS-Protection` (legacy browser support)
- `Referrer-Policy`

**Files**:
- `my-website-backend/src/streaming_handler.py:75-84`

**Current State**:
```python
# Streaming endpoint has minimal headers
"Content-Type": "application/x-ndjson",
"Cache-Control": "no-cache",
"Access-Control-Allow-Origin": "*",  # Should be restricted
```

#### 4. No Web Application Firewall (WAF)
**Severity**: HIGH
**Impact**: No protection against common web exploits and bots

**Missing Protections**:
- SQL/NoSQL injection filtering
- Bot detection and mitigation
- Request size limits
- Geographic blocking capabilities
- IP reputation filtering

#### 5. Broad IAM Permissions
**Severity**: MEDIUM
**Impact**: Excessive permissions could be exploited

**Issue**:
```yaml
# serverless.yml:46-49
- Effect: Allow
  Action:
    - bedrock-agentcore:InvokeAgentRuntime
  Resource: "*"  # Should be scoped to specific agent ARN
```

**Fix**: Replace with:
```yaml
Resource: "arn:aws:bedrock-agentcore:ap-southeast-2:136079914867:runtime/website_agentV2-ZY35by5UAQ"
```

### Medium Risk

#### 6. Wildcard CORS on Streaming Endpoint
**Severity**: MEDIUM
**Location**: `my-website-backend/src/streaming_handler.py:75-84`

**Issue**:
```python
"Access-Control-Allow-Origin": "*"
```

**Should be**:
```python
"Access-Control-Allow-Origin": "https://sushensatturu.com"
```

#### 7. No Request Size Validation
**Severity**: MEDIUM
**Impact**: Large payloads could increase costs or cause errors

**Missing Validations**:
- Chat message content length limits
- File upload size restrictions (if implemented)
- Blog post content size limits

#### 8. No Security Monitoring
**Severity**: MEDIUM
**Impact**: Cannot detect or respond to attacks in real-time

**Missing**:
- CloudWatch security event logging
- Failed authentication attempt tracking
- Suspicious activity alerts
- Cost anomaly detection

---

## DDoS Protection

### Understanding DDoS Attacks

**Distributed Denial of Service (DDoS)** attacks overwhelm your services with traffic from multiple sources, making them unavailable to legitimate users. For serverless architectures, DDoS attacks primarily impact:

1. **Cost**: Lambda invocations and Bedrock API calls cost money per request
2. **Availability**: Overwhelming backend services
3. **Reputation**: Slow or unavailable site damages user trust

### Current DDoS Protection

#### AWS Shield Standard (Enabled)
- **Cost**: Free (automatically included)
- **Protection**: Layer 3/4 DDoS attacks (network/transport layer)
- **Coverage**: CloudFront and API Gateway
- **Limitations**: No application-layer (Layer 7) protection

### Recommended DDoS Protection Strategy

#### Tier 1: Basic Protection (Recommended for Personal Sites)

**1. AWS WAF with Rate Limiting**
- **Cost**: ~$5-10/month for typical traffic
- **Protection**: Rate-based rules, common attack patterns
- **Implementation**: See [WAF Configuration](#waf-configuration)

**2. API Gateway Throttling**
- **Cost**: Free
- **Protection**: Per-second request limits
- **Implementation**: See [API Gateway Throttling](#api-gateway-throttling)

**3. Application-Level Rate Limiting**
- **Cost**: Free
- **Protection**: Per-IP request limits
- **Implementation**: See [Rate Limiting Middleware](#rate-limiting-middleware)

#### Tier 2: Advanced Protection (If Becoming a Target)

**AWS Shield Advanced**
- **Cost**: $3,000/month
- **Benefits**:
  - 24/7 DDoS Response Team (DRT)
  - Cost protection (refunds for DDoS-related scaling)
  - Advanced real-time metrics and reports
  - Layer 7 attack protection

**When to consider**: Only if experiencing sustained, sophisticated DDoS attacks

---

## Implementation Guides

### WAF Configuration

Add AWS WAF to protect against Layer 7 attacks and implement rate limiting.

**1. Add to `my-website-backend/serverless.yml` in the `resources.Resources` section:**

```yaml
# AWS WAF WebACL
PortfolioWebACL:
  Type: AWS::WAFv2::WebACL
  Properties:
    Name: ${self:provider.stage}-portfolio-waf
    Scope: REGIONAL
    DefaultAction:
      Allow: {}
    Rules:
      # Rate-based rule for DDoS protection
      - Name: RateLimitRule
        Priority: 1
        Statement:
          RateBasedStatement:
            Limit: 2000  # Requests per 5 minutes per IP
            AggregateKeyType: IP
        Action:
          Block: {}
        VisibilityConfig:
          SampledRequestsEnabled: true
          CloudWatchMetricsEnabled: true
          MetricName: RateLimitRule

      # AWS Managed Rules - Common vulnerabilities
      - Name: AWSManagedRulesCommonRuleSet
        Priority: 2
        Statement:
          ManagedRuleGroupStatement:
            VendorName: AWS
            Name: AWSManagedRulesCommonRuleSet
            ExcludedRules: []
        OverrideAction:
          None: {}
        VisibilityConfig:
          SampledRequestsEnabled: true
          CloudWatchMetricsEnabled: true
          MetricName: AWSManagedRulesCommon

      # Known bad inputs
      - Name: AWSManagedRulesKnownBadInputsRuleSet
        Priority: 3
        Statement:
          ManagedRuleGroupStatement:
            VendorName: AWS
            Name: AWSManagedRulesKnownBadInputsRuleSet
        OverrideAction:
          None: {}
        VisibilityConfig:
          SampledRequestsEnabled: true
          CloudWatchMetricsEnabled: true
          MetricName: AWSManagedRulesKnownBadInputs

      # Optional: Bot Control (costs ~$10/month)
      # - Name: AWSManagedRulesBotControlRuleSet
      #   Priority: 4
      #   Statement:
      #     ManagedRuleGroupStatement:
      #       VendorName: AWS
      #       Name: AWSManagedRulesBotControlRuleSet
      #   OverrideAction:
      #     None: {}
      #   VisibilityConfig:
      #     SampledRequestsEnabled: true
      #     CloudWatchMetricsEnabled: true
      #     MetricName: BotControl

    VisibilityConfig:
      SampledRequestsEnabled: true
      CloudWatchMetricsEnabled: true
      MetricName: ${self:provider.stage}-portfolio-waf

# Associate WAF with API Gateway
PortfolioWebACLAssociation:
  Type: AWS::WAFv2::WebACLAssociation
  Properties:
    ResourceArn:
      Fn::Sub: arn:aws:apigateway:${AWS::Region}::/restapis/${ApiGatewayRestApi}/stages/${self:provider.stage}
    WebACLArn:
      Fn::GetAtt: [PortfolioWebACL, Arn]
```

**2. Deploy:**
```bash
cd my-website-backend
serverless deploy --stage prod
```

**3. Monitor:**
- AWS Console → WAF & Shield → Web ACLs → View metrics
- CloudWatch dashboard for blocked requests

### API Gateway Throttling

Configure request limits at the API Gateway level.

**Add to `my-website-backend/serverless.yml` under the `provider` section:**

```yaml
provider:
  name: aws
  runtime: python3.11
  # ... existing config ...

  # API Gateway throttling settings
  apiGateway:
    usagePlan:
      quota:
        limit: 10000      # Total requests per day
        period: DAY
      throttle:
        rateLimit: 10     # Steady-state requests per second
        burstLimit: 20    # Burst capacity

    # Optional: Create API keys for monitoring
    apiKeys:
      - name: ${self:provider.stage}-portfolio-api-key
        description: "API key for monitoring usage"
```

**Configuration Guidelines**:
- `rateLimit`: Average requests per second (start with 10 for personal site)
- `burstLimit`: Maximum concurrent requests (typically 2x rateLimit)
- `quota.limit`: Daily request limit (adjust based on expected traffic)

### Rate Limiting Middleware

Implement application-level rate limiting for fine-grained control.

**1. Create `my-website-backend/src/middleware/rate_limiter.py`:**

```python
"""
Rate limiting middleware for FastAPI.
Prevents API abuse by limiting requests per IP address.
"""
from fastapi import Request, HTTPException
from collections import defaultdict
import time
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Simple in-memory rate limiter based on IP address.

    Note: This is suitable for single-instance Lambda functions.
    For multi-instance deployments, consider using Redis or DynamoDB.
    """

    def __init__(self, requests_per_minute: int = 10):
        """
        Initialize rate limiter.

        Args:
            requests_per_minute: Maximum requests allowed per IP per minute
        """
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.limit = requests_per_minute
        self.window_seconds = 60

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP from request headers."""
        # API Gateway forwards client IP in X-Forwarded-For header
        forwarded_for = request.headers.get("X-Forwarded-For", "")
        if forwarded_for:
            # X-Forwarded-For format: "client, proxy1, proxy2"
            return forwarded_for.split(",")[0].strip()

        # Fallback to direct client
        return request.client.host if request.client else "unknown"

    def _clean_old_requests(self, ip: str, now: float):
        """Remove requests outside the time window."""
        self.requests[ip] = [
            req_time for req_time in self.requests[ip]
            if now - req_time < self.window_seconds
        ]

    async def check_rate_limit(self, request: Request) -> None:
        """
        Check if request exceeds rate limit.

        Raises:
            HTTPException: 429 Too Many Requests if limit exceeded
        """
        client_ip = self._get_client_ip(request)
        now = time.time()

        # Clean old requests
        self._clean_old_requests(client_ip, now)

        # Check limit
        request_count = len(self.requests[client_ip])
        if request_count >= self.limit:
            logger.warning(
                f"Rate limit exceeded for IP {client_ip}: "
                f"{request_count} requests in last {self.window_seconds}s"
            )
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "RateLimitExceeded",
                    "message": f"Too many requests. Maximum {self.limit} requests per minute.",
                    "retry_after": 60
                }
            )

        # Record request
        self.requests[client_ip].append(now)
        logger.debug(f"Request from {client_ip}: {request_count + 1}/{self.limit}")


# Create rate limiter instances for different endpoints
chat_rate_limiter = RateLimiter(requests_per_minute=10)  # Strict for expensive AI calls
blog_rate_limiter = RateLimiter(requests_per_minute=30)  # More lenient for blog reads
```

**2. Update `my-website-backend/src/handlers/chat.py` to use rate limiting:**

```python
from fastapi import APIRouter, Depends
from ..middleware.rate_limiter import chat_rate_limiter

router = APIRouter()

@router.post("/chat")
async def chat(
    request: ChatRequest,
    _: None = Depends(chat_rate_limiter.check_rate_limit)  # Add rate limiting
):
    # ... existing chat handler code ...
    pass
```

**3. Update `my-website-backend/src/handlers/blog.py`:**

```python
from fastapi import APIRouter, Depends
from ..middleware.rate_limiter import blog_rate_limiter

router = APIRouter()

@router.get("/blog/posts")
async def get_posts(
    _: None = Depends(blog_rate_limiter.check_rate_limit)
):
    # ... existing code ...
    pass
```

### Security Headers Middleware

Protect against common browser-based attacks.

**1. Create `my-website-backend/src/middleware/security_headers.py`:**

```python
"""
Security headers middleware for FastAPI.
Adds security-related HTTP headers to all responses.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add security headers to all HTTP responses.

    Headers included:
    - X-Content-Type-Options: Prevent MIME type sniffing
    - X-Frame-Options: Prevent clickjacking
    - X-XSS-Protection: Enable browser XSS filters (legacy)
    - Strict-Transport-Security: Enforce HTTPS
    - Content-Security-Policy: Control resource loading
    - Referrer-Policy: Control referrer information
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking - don't allow site to be framed
        response.headers["X-Frame-Options"] = "DENY"

        # Legacy XSS protection for older browsers
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Enforce HTTPS (only send over secure connections)
        # max-age: 1 year, includeSubDomains: apply to all subdomains
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        # Content Security Policy - restrict resource loading
        # Adjust based on your needs (this is restrictive)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "  # Adjust for Next.js
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' https://sushensatturu.com; "
            "frame-ancestors 'none';"
        )

        # Control referrer information sent to external sites
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Remove server information disclosure
        response.headers.pop("Server", None)

        return response
```

**2. Update `my-website-backend/src/main.py`:**

```python
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from .middleware.security_headers import SecurityHeadersMiddleware
from .middleware.error_handler import add_exception_handlers

app = FastAPI()

# Add security headers to all responses
app.add_middleware(SecurityHeadersMiddleware)

# Only allow requests from trusted hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "sushensatturu.com",
        "*.execute-api.ap-southeast-2.amazonaws.com",
        "*.lambda-url.ap-southeast-2.on.aws"
    ]
)

# ... rest of your app setup ...
```

### API Key Authentication

Protect expensive endpoints (like chat) with simple API key authentication.

**1. Create `my-website-backend/src/middleware/auth.py`:**

```python
"""
API key authentication for FastAPI.
Protects endpoints that incur costs (e.g., AI chat).
"""
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import os
import logging

logger = logging.getLogger(__name__)

# Define API key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Verify API key from request header.

    Args:
        api_key: API key from X-API-Key header

    Returns:
        The validated API key

    Raises:
        HTTPException: 403 if API key is invalid or missing
    """
    # Get valid API key from environment (stored in Secrets Manager)
    valid_key = os.environ.get("PORTFOLIO_API_KEY")

    if not valid_key:
        logger.error("PORTFOLIO_API_KEY environment variable not set")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error"
        )

    if not api_key:
        logger.warning("Request missing API key")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "MissingAPIKey",
                "message": "API key required. Include X-API-Key header."
            }
        )

    if api_key != valid_key:
        logger.warning(f"Invalid API key attempted: {api_key[:8]}...")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "InvalidAPIKey",
                "message": "Invalid API key"
            }
        )

    logger.debug("API key validated successfully")
    return api_key
```

**2. Update chat handler to require API key:**

```python
from fastapi import APIRouter, Depends
from ..middleware.auth import verify_api_key
from ..middleware.rate_limiter import chat_rate_limiter

router = APIRouter()

@router.post("/chat")
async def chat(
    request: ChatRequest,
    _rate_limit: None = Depends(chat_rate_limiter.check_rate_limit),
    _api_key: str = Depends(verify_api_key)  # Require API key
):
    # ... existing chat handler code ...
    pass
```

**3. Store API key in Secrets Manager:**

```bash
# Generate secure random API key
export API_KEY=$(openssl rand -hex 32)

# Store in Secrets Manager
aws secretsmanager create-secret \
    --name prod/portfolio/api-key \
    --secret-string "$API_KEY" \
    --region ap-southeast-2

# Update Lambda environment to load from Secrets Manager
```

**4. Update frontend to include API key:**

```typescript
// my-website-frontend/src/components/Chatbot.tsx
const response = await fetch(`${API_URL}/chat`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': process.env.NEXT_PUBLIC_API_KEY || ''
  },
  body: JSON.stringify(chatRequest)
});
```

---

## Security Best Practices

### Development Practices

1. **Never commit secrets**
   - Use `.env.example` for documentation
   - Store production secrets in AWS Secrets Manager
   - Use environment-specific configurations

2. **Input validation**
   - Validate all user inputs with Pydantic models
   - Sanitize HTML content with DOMPurify
   - Limit request payload sizes

3. **Error handling**
   - Never expose internal error details in production
   - Log detailed errors server-side only
   - Use appropriate HTTP status codes

4. **Dependencies**
   - Regularly update dependencies: `npm audit`, `pip-audit`
   - Review security advisories
   - Use Dependabot or Renovate for automated updates

### Deployment Practices

1. **Least privilege IAM**
   - Grant minimum required permissions
   - Use specific resource ARNs (avoid wildcards)
   - Regularly review and audit IAM policies

2. **Network security**
   - Keep Lambda in AWS-managed VPC (no VPC needed for public APIs)
   - Use private subnets if accessing RDS or other VPC resources
   - Enable VPC Flow Logs for network monitoring

3. **Encryption**
   - Enable encryption at rest for DynamoDB (default)
   - Use HTTPS only (CloudFront enforces this)
   - Enable S3 bucket encryption for frontend assets

4. **Monitoring**
   - Enable CloudWatch Logs for all Lambda functions
   - Set up CloudWatch Alarms for errors and costs
   - Review AWS Trusted Advisor recommendations

### Code Review Checklist

Before deploying changes:

- [ ] No hardcoded secrets or API keys
- [ ] Input validation on all user inputs
- [ ] Rate limiting on expensive operations
- [ ] Error messages don't expose sensitive data
- [ ] Authentication required for protected endpoints
- [ ] CORS configured correctly (no wildcards in production)
- [ ] Dependencies up to date with no known vulnerabilities
- [ ] IAM permissions follow least privilege
- [ ] CloudWatch logging enabled
- [ ] Security headers configured

---

## Monitoring and Alerts

### CloudWatch Alarms

**1. Cost Alerts for Bedrock**

Add to `my-website-backend/serverless.yml`:

```yaml
BedrockCostAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    AlarmName: ${self:provider.stage}-bedrock-high-cost
    AlarmDescription: Alert when Bedrock costs exceed threshold
    MetricName: EstimatedCharges
    Namespace: AWS/Billing
    Statistic: Maximum
    Period: 21600  # 6 hours
    EvaluationPeriods: 1
    Threshold: 10  # Alert if estimated charges > $10
    ComparisonOperator: GreaterThanThreshold
    Dimensions:
      - Name: ServiceName
        Value: AWSBedrock
    # Optional: Add SNS topic for notifications
    # AlarmActions:
    #   - Ref: AlertTopic

LambdaErrorAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    AlarmName: ${self:provider.stage}-lambda-errors
    AlarmDescription: Alert on Lambda function errors
    MetricName: Errors
    Namespace: AWS/Lambda
    Statistic: Sum
    Period: 300  # 5 minutes
    EvaluationPeriods: 1
    Threshold: 10  # Alert if > 10 errors in 5 minutes
    ComparisonOperator: GreaterThanThreshold
    Dimensions:
      - Name: FunctionName
        Value:
          Ref: ApiLambdaFunction

ThrottlingAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    AlarmName: ${self:provider.stage}-api-throttling
    AlarmDescription: Alert when requests are being throttled
    MetricName: Throttles
    Namespace: AWS/Lambda
    Statistic: Sum
    Period: 300
    EvaluationPeriods: 1
    Threshold: 50  # Alert if > 50 throttled requests
    ComparisonOperator: GreaterThanThreshold
    Dimensions:
      - Name: FunctionName
        Value:
          Ref: ApiLambdaFunction
```

**2. Enable CloudWatch Logs Insights Queries**

Useful queries for security monitoring:

```sql
-- Find rate limit violations
fields @timestamp, @message
| filter @message like /Rate limit exceeded/
| stats count() by bin(5m)

-- Find failed authentication attempts
fields @timestamp, @message
| filter @message like /Invalid API key/
| stats count() by bin(1h)

-- Find expensive operations
fields @timestamp, @duration, @message
| filter @duration > 5000
| sort @duration desc
| limit 20

-- Monitor error rates
fields @timestamp, @message
| filter @level = "ERROR"
| stats count() by bin(5m)
```

### Security Logging

**Enable comprehensive logging in `my-website-backend/src/main.py`:**

```python
import logging
import json
from datetime import datetime

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security event logger
security_logger = logging.getLogger("security")

def log_security_event(event_type: str, details: dict):
    """Log security-related events for monitoring."""
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "details": details
    }
    security_logger.warning(json.dumps(event))

# Use in your middleware
# log_security_event("rate_limit_exceeded", {"ip": client_ip, "endpoint": "/chat"})
# log_security_event("invalid_api_key", {"ip": client_ip})
```

---

## Cost Considerations

### Current Infrastructure Costs

**Estimated monthly costs for low-moderate traffic (10,000 requests/month):**

| Service | Cost | Notes |
|---------|------|-------|
| API Gateway | $0.03 | First 333M requests: $1.00 per million |
| Lambda | $0.20 | 512MB, 1s avg duration |
| DynamoDB | $1.25 | On-demand pricing, light usage |
| CloudFront | $0.50 | 1GB transfer + requests |
| S3 | $0.10 | Static hosting |
| Secrets Manager | $0.40 | $0.40 per secret/month |
| **Subtotal** | **$2.48** | |

**Variable costs:**
| Service | Cost | Risk |
|---------|------|------|
| AWS Bedrock | Variable | $3-15 per 1M tokens (depends on model) |

### Security Features Cost Impact

**Recommended (Low Cost):**
| Feature | Monthly Cost | Value |
|---------|-------------|-------|
| WAF - Common Rules | $5.00 | Rate limiting + basic protection |
| WAF - Requests | $0.60 | Per million requests |
| CloudWatch Alarms | $0.10 | First 10 alarms free |
| **Total** | **~$5.70** | **Essential protection** |

**Optional (Higher Cost):**
| Feature | Monthly Cost | When Needed |
|---------|-------------|-------------|
| WAF - Bot Control | $10.00 | If seeing bot traffic |
| Shield Advanced | $3,000 | Only if actively targeted |
| GuardDuty | $4.62 | Advanced threat detection |

### Cost Protection Strategy

1. **Set billing alerts** at $10, $25, $50, $100 thresholds
2. **Monitor Bedrock usage** - Most variable cost component
3. **Review CloudWatch costs** - Log retention can add up
4. **Use AWS Cost Explorer** - Analyze spending patterns monthly

**Cost optimization tips:**
- Set CloudWatch Logs retention to 7-30 days (not indefinite)
- Use DynamoDB on-demand billing for variable traffic
- Enable S3 lifecycle policies for old assets
- Review and remove unused resources monthly

---

## Incident Response Plan

### If Under DDoS Attack

1. **Immediate Actions**
   - Check CloudWatch metrics for traffic patterns
   - Review WAF blocked requests in AWS Console
   - Identify attack source IPs

2. **Mitigation Steps**
   - Increase WAF rate limits if legitimate traffic affected
   - Add IP-based block rules in WAF for known attackers
   - Temporarily reduce Lambda concurrency limit to control costs
   - Consider enabling Shield Advanced for DRT support

3. **Cost Control**
   - Set Lambda reserved concurrency to limit invocations
   - Monitor AWS billing in real-time
   - Contact AWS Support for billing protection

### If API Key Compromised

1. **Immediately rotate API key** in Secrets Manager
2. **Review CloudWatch Logs** for unauthorized usage
3. **Check billing** for unexpected charges
4. **Update frontend** with new API key
5. **Add IP allowlist** if attackers identified

### If Vulnerability Discovered

1. **Assess severity** and impact
2. **Deploy fix immediately** to production
3. **Review logs** for exploitation attempts
4. **Notify users** if data compromised (legal requirement in many jurisdictions)
5. **Document incident** and update security procedures

---

## Compliance and Best Practices

### Data Privacy

**Current data collection:**
- Chat conversations (with TTL - auto-deleted)
- Blog view counts
- No personally identifiable information (PII)

**Recommendations:**
- Add privacy policy to website
- Document data retention policies
- Implement user data deletion on request
- Consider GDPR compliance if EU users

### Accessibility

**Security should not compromise accessibility:**
- Rate limiting should allow reasonable usage
- Error messages should be clear and helpful
- CAPTCHA (if implemented) should have audio alternative
- Security headers should not break screen readers

---

## Security Roadmap

### Phase 1: Critical Security (Week 1-2)
- [ ] Implement AWS WAF with rate limiting
- [ ] Add API key authentication for chat endpoint
- [ ] Configure API Gateway throttling
- [ ] Add security headers middleware
- [ ] Set up cost alerts for Bedrock
- [ ] Enable CloudWatch logging

### Phase 2: Enhanced Protection (Week 3-4)
- [ ] Implement application-level rate limiting
- [ ] Fix IAM permission wildcards
- [ ] Add request size validation
- [ ] Set up security event logging
- [ ] Create CloudWatch dashboard for monitoring
- [ ] Document incident response procedures

### Phase 3: Advanced Security (Month 2)
- [ ] Implement proper authentication (OAuth/JWT) if blog write operations needed
- [ ] Add CAPTCHA to chat endpoint
- [ ] Enable DynamoDB point-in-time recovery
- [ ] Set up automated security scanning (Dependabot)
- [ ] Implement session-based rate limiting
- [ ] Add geographic blocking in WAF if needed

### Phase 4: Ongoing Maintenance
- [ ] Monthly dependency updates
- [ ] Quarterly security audits
- [ ] Review and rotate API keys every 90 days
- [ ] Monitor and respond to AWS security bulletins
- [ ] Review CloudWatch Logs Insights for anomalies

---

## Resources

### AWS Documentation
- [AWS WAF Developer Guide](https://docs.aws.amazon.com/waf/latest/developerguide/)
- [AWS Shield Documentation](https://docs.aws.amazon.com/shield/latest/developerguide/)
- [API Gateway Throttling](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)
- [Lambda Security Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/lambda-security.html)

### Security Standards
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [AWS Well-Architected Framework - Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/)

### Tools
- [npm audit](https://docs.npmjs.com/cli/v8/commands/npm-audit) - Check Node.js dependencies
- [pip-audit](https://pypi.org/project/pip-audit/) - Check Python dependencies
- [AWS Trusted Advisor](https://aws.amazon.com/premiumsupport/technology/trusted-advisor/) - Security recommendations
- [AWS Security Hub](https://aws.amazon.com/security-hub/) - Centralized security findings

---

## Questions or Concerns?

For security issues or questions about this documentation:
1. Review the [Implementation Guides](#implementation-guides) section
2. Check AWS documentation for specific services
3. Consider consulting with a security professional for production deployments

**Remember**: Security is an ongoing process, not a one-time implementation. Regularly review and update your security posture as threats evolve.
