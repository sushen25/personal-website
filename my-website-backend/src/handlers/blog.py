"""
Blog API route handlers.
"""

from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional, Dict, Any

from src.models.schemas import BlogPost, BlogPostSummary
from src.middleware.error_handler import NotFoundError, ValidationError

# Create router
router = APIRouter()

# Import blog_service after router creation to avoid circular imports
# The service will be imported when the module loads
from src.utils.dynamodb import blog_db
from src.services.blog_service import BlogService

# Initialize blog service
blog_service = BlogService(blog_db)


@router.post("", response_model=BlogPost, status_code=status.HTTP_201_CREATED)
async def create_post(post: BlogPost) -> BlogPost:
    """
    Create a new blog post.

    Automatically extracts text content from HTML if not provided.

    Args:
        post: BlogPost object with content

    Returns:
        Created BlogPost with all fields populated

    Raises:
        HTTPException: If creation fails or validation error
    """
    try:
        response = await blog_service.create_post(post)
        return response

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error in create_post endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create blog post: {str(e)}"
        )


@router.get("", response_model=List[BlogPostSummary])
async def list_posts(
    status_filter: str = Query(default="published", alias="status", description="Filter by post status"),
    limit: int = Query(default=100, ge=1, le=100, description="Maximum number of posts to return")
) -> List[BlogPostSummary]:
    """
    List blog posts filtered by status, sorted by creation date (newest first).

    Args:
        status_filter: Post status (published, draft, archived)
        limit: Maximum number of posts to return

    Returns:
        List of BlogPostSummary objects

    Raises:
        HTTPException: If listing fails
    """
    try:
        posts = await blog_service.list_posts(status=status_filter, limit=limit)
        return posts

    except Exception as e:
        print(f"Error in list_posts endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list blog posts: {str(e)}"
        )


@router.get("/{slug}", response_model=BlogPost)
async def get_post(slug: str) -> BlogPost:
    """
    Get a specific blog post by slug.

    Args:
        slug: Post slug (URL-friendly identifier)

    Returns:
        BlogPost with full content

    Raises:
        HTTPException: If post not found or retrieval fails
    """
    try:
        post = await blog_service.get_post_by_slug(slug)

        # Optionally increment view count
        # Uncomment the next line if you want to track views
        # await blog_service.increment_view_count(slug)

        return post

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error in get_post endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve blog post: {str(e)}"
        )


@router.put("/{slug}", response_model=BlogPost)
async def update_post(slug: str, updates: Dict[str, Any]) -> BlogPost:
    """
    Update a blog post.

    If html_content is updated, text_content is automatically re-extracted.

    Args:
        slug: Post slug to update
        updates: Dictionary of fields to update

    Returns:
        Updated BlogPost

    Raises:
        HTTPException: If post not found or update fails
    """
    try:
        post = await blog_service.update_post(slug, updates)
        return post

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error in update_post endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update blog post: {str(e)}"
        )


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(slug: str):
    """
    Delete a blog post.

    Args:
        slug: Post slug to delete

    Raises:
        HTTPException: If post not found or deletion fails
    """
    try:
        success = await blog_service.delete_post(slug)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Blog post not found: {slug}"
            )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in delete_post endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete blog post: {str(e)}"
        )


@router.post("/{slug}/view", response_model=Dict[str, int])
async def increment_view_count(slug: str) -> Dict[str, int]:
    """
    Increment view count for a blog post.

    Args:
        slug: Post slug

    Returns:
        Dictionary with new view count

    Raises:
        HTTPException: If post not found
    """
    try:
        new_count = await blog_service.increment_view_count(slug)
        return {"view_count": new_count}

    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error in increment_view_count endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to increment view count: {str(e)}"
        )
