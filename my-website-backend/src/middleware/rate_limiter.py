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
    Simple in-memory rate limiter.

    Note: This is suitable for single-instance Lambda functions.
    For multi-instance deployments, consider using Redis or DynamoDB.
    """

    def __init__(self, requests_per_minute: int = 10, window_seconds: int = 60, global_limit: bool = True):
        """
        Initialize rate limiter.

        Args:
            requests_per_minute: Maximum requests allowed per window
            window_seconds: Time window in seconds (default 60)
            global_limit: If True, limit applies globally across all IPs. If False, limit per IP.
        """
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.global_requests: List[float] = []
        self.limit = requests_per_minute
        self.window_seconds = window_seconds
        self.global_limit = global_limit

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
        if self.global_limit:
            self.global_requests = [
                req_time for req_time in self.global_requests
                if now - req_time < self.window_seconds
            ]
        else:
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
        if self.global_limit:
            request_count = len(self.global_requests)
            if request_count >= self.limit:
                retry_after = int(self.window_seconds - (now - self.global_requests[0]))
                logger.warning(
                    f"Global rate limit exceeded: "
                    f"{request_count} requests in last {self.window_seconds}s"
                )
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "RateLimitExceeded",
                        "message": f"Service is currently at capacity. Maximum {self.limit} requests per {self.window_seconds} seconds.",
                        "retry_after": max(retry_after, 1)
                    },
                    headers={"Retry-After": str(max(retry_after, 1))}
                )
            # Record request
            self.global_requests.append(now)
            logger.debug(f"Global request count: {request_count + 1}/{self.limit}")
        else:
            request_count = len(self.requests[client_ip])
            if request_count >= self.limit:
                retry_after = int(self.window_seconds - (now - self.requests[client_ip][0]))
                logger.warning(
                    f"Rate limit exceeded for IP {client_ip}: "
                    f"{request_count} requests in last {self.window_seconds}s"
                )
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "RateLimitExceeded",
                        "message": f"Too many requests. Maximum {self.limit} requests per {self.window_seconds} seconds.",
                        "retry_after": max(retry_after, 1)
                    },
                    headers={"Retry-After": str(max(retry_after, 1))}
                )
            # Record request
            self.requests[client_ip].append(now)
            logger.debug(f"Request from {client_ip}: {request_count + 1}/{self.limit}")


# Create rate limiter instances for different endpoints
# Chat endpoint: global limit to control total costs
chat_rate_limiter = RateLimiter(requests_per_minute=20, window_seconds=60, global_limit=True)

# Blog endpoints: more lenient (cheaper operations)
blog_rate_limiter = RateLimiter(requests_per_minute=100, window_seconds=60, global_limit=True)
