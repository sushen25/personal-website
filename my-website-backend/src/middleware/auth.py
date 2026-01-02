"""
API key authentication for FastAPI.
Protects endpoints that incur costs (e.g., AI chat).
"""
import os
from fastapi import Security, HTTPException, status, Request
from fastapi.security import APIKeyHeader
from typing import Optional
import logging
from ..utils.secrets_manager import SecretsManager

logger = logging.getLogger(__name__)

IS_LOCAL = os.getenv("STAGE", "dev") == "local" or os.getenv("IS_LOCAL", "false").lower() == "true"

# Define API key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Initialize secrets manager
secrets_manager = SecretsManager()


async def verify_api_key(
    request: Request,
    api_key: Optional[str] = Security(api_key_header)
) -> str:
    """
    Verify API key from request header.

    Args:
        request: FastAPI request object
        api_key: API key from X-API-Key header

    Returns:
        The validated API key

    Raises:
        HTTPException: 403 if API key is invalid or missing
    """
    print("Authenticating request")
    # Get client IP for logging
    client_ip = request.headers.get("X-Forwarded-For", "unknown").split(",")[0].strip()

    if not api_key:
        logger.warning(f"Request missing API key from IP {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "MissingAPIKey",
                "message": "API key required. Include X-API-Key header in your request."
            }
        )

    # Get valid API key from Secrets Manager
    try:
        print("Fetching Secret, LOCAL: ", IS_LOCAL)
        if IS_LOCAL:
            valid_key = "local-api-key"
        else:
            valid_key = secrets_manager.get_secret("dev-portfolio-api-key")
    except Exception as e:
        logger.error(f"Failed to retrieve API key from Secrets Manager: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalServerError",
                "message": "Server configuration error"
            }
        )

    

    print("VALID KEY: ", valid_key)
    print("INVALID KEY: ", api_key)

    if api_key != valid_key:
        logger.warning(f"Invalid API key attempted from IP {client_ip}: {api_key[:8]}...")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "InvalidAPIKey",
                "message": "Invalid API key provided"
            }
        )

    logger.debug(f"API key validated successfully for IP {client_ip}")
    return api_key


async def verify_api_key_optional(
    api_key: Optional[str] = Security(api_key_header)
) -> Optional[str]:
    """
    Optional API key verification.
    Allows requests without API key but logs them.
    Useful for gradual migration or read-only endpoints.

    Args:
        api_key: API key from X-API-Key header

    Returns:
        The API key if provided and valid, None otherwise
    """
    if not api_key:
        return None

    try:
        valid_key = secrets_manager.get_secret("portfolio-api-key")
        if api_key == valid_key:
            logger.debug("Valid API key provided")
            return api_key
        else:
            logger.warning(f"Invalid API key provided: {api_key[:8]}...")
            return None
    except Exception as e:
        logger.error(f"Error validating API key: {str(e)}")
        return None
