"""
Global error handling middleware for FastAPI.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AppError(Exception):
    """Base application error with status code."""

    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, detail: dict = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}
        super().__init__(self.message)


class NotFoundError(AppError):
    """Resource not found error."""

    def __init__(self, message: str = "Resource not found", detail: dict = None):
        super().__init__(message, status.HTTP_404_NOT_FOUND, detail)


class ValidationError(AppError):
    """Validation error."""

    def __init__(self, message: str = "Validation failed", detail: dict = None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, detail)


class UnauthorizedError(AppError):
    """Unauthorized error."""

    def __init__(self, message: str = "Unauthorized", detail: dict = None):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, detail)


class ForbiddenError(AppError):
    """Forbidden error."""

    def __init__(self, message: str = "Forbidden", detail: dict = None):
        super().__init__(message, status.HTTP_403_FORBIDDEN, detail)


class AgentServiceError(AppError):
    """Error from Agent Service."""

    def __init__(self, message: str = "Agent service error", detail: dict = None):
        super().__init__(message, status.HTTP_503_SERVICE_UNAVAILABLE, detail)


def add_exception_handlers(app: FastAPI) -> None:
    """
    Add all exception handlers to the FastAPI application.

    Args:
        app: FastAPI application instance
    """

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        """Handle custom application errors."""
        logger.error(f"AppError: {exc.message} - Status: {exc.status_code} - Detail: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.__class__.__name__,
                "message": exc.message,
                "status_code": exc.status_code,
                "detail": exc.detail
            }
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Handle HTTP exceptions."""
        logger.error(f"HTTPException: {exc.detail} - Status: {exc.status_code}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "HTTPException",
                "message": str(exc.detail),
                "status_code": exc.status_code,
                "detail": {}
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle Pydantic validation errors."""
        logger.error(f"ValidationError: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "ValidationError",
                "message": "Request validation failed",
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "detail": {
                    "errors": exc.errors()
                }
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all other exceptions."""
        # Log the full traceback for debugging
        logger.error(f"Unhandled exception: {str(exc)}")
        logger.error(traceback.format_exc())

        # Don't expose internal error details in production
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "InternalServerError",
                "message": "An internal server error occurred",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "detail": {}
            }
        )
