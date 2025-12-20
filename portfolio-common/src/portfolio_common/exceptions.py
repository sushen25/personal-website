"""
Shared exception classes for portfolio services.
"""


class PortfolioError(Exception):
    """Base exception for portfolio operations."""

    def __init__(self, message: str, detail: dict = None):
        self.message = message
        self.detail = detail or {}
        super().__init__(self.message)


class NotFoundError(PortfolioError):
    """Resource not found error."""
    pass


class ValidationError(PortfolioError):
    """Validation error."""
    pass


class UnauthorizedError(PortfolioError):
    """Unauthorized access error."""
    pass


class ForbiddenError(PortfolioError):
    """Forbidden access error."""
    pass
