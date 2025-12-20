"""
Blog service - wrapper around shared portfolio-common package with exception translation.
"""

from typing import List, Dict, Any
from portfolio_common.services.blog_service import BlogService as SharedBlogService
from portfolio_common.models.schemas import BlogPost, BlogPostSummary
from portfolio_common.exceptions import (
    NotFoundError as SharedNotFoundError,
    ValidationError as SharedValidationError,
)
from src.middleware.error_handler import NotFoundError, ValidationError


class BlogService(SharedBlogService):
    """
    Blog service that wraps the shared BlogService and translates exceptions
    to backend-specific middleware exceptions.
    """

    async def get_post_by_slug(self, slug: str) -> BlogPost:
        """Get a blog post by slug, translating exceptions."""
        try:
            return await super().get_post_by_slug(slug)
        except SharedNotFoundError as e:
            raise NotFoundError(message=e.message, detail=e.detail)

    async def create_post(self, post: BlogPost) -> BlogPost:
        """Create a blog post, translating exceptions."""
        try:
            return await super().create_post(post)
        except SharedValidationError as e:
            raise ValidationError(message=e.message, detail=e.detail)

    async def update_post(self, slug: str, updates: Dict[str, Any]) -> BlogPost:
        """Update a blog post, translating exceptions."""
        try:
            return await super().update_post(slug, updates)
        except SharedNotFoundError as e:
            raise NotFoundError(message=e.message, detail=e.detail)
        except SharedValidationError as e:
            raise ValidationError(message=e.message, detail=e.detail)

    async def increment_view_count(self, slug: str) -> int:
        """Increment view count, translating exceptions."""
        try:
            return await super().increment_view_count(slug)
        except SharedNotFoundError as e:
            raise NotFoundError(message=e.message, detail=e.detail)

    # delete_post and list_posts don't throw the shared exceptions we need to translate,
    # so they can be inherited as-is
