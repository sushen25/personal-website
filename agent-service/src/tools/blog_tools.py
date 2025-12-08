"""
Custom tools for blog content queries.
"""

from strands import tool
from typing import List, Dict, Any, Optional
from src.services.content_service import content_service


@tool
def search_blog_posts(query: str) -> List[Dict[str, Any]]:
    """
    Search blog posts by title, tags, or content.

    Use this tool when users ask about blog posts, articles, or want to find content
    about a specific topic. The search looks through post titles, excerpts, content, and tags.

    Args:
        query: Search query string (e.g., "AI", "Python", "AWS")

    Returns:
        List of matching blog posts with title, slug, excerpt, published date, and tags
    """
    return content_service.search_blog_posts(query)


@tool
def get_blog_post(slug: str) -> Dict[str, Any]:
    """
    Fetch full blog post by slug.

    Use this tool when users ask for a specific blog post or want to read a full article.
    The slug is typically the URL-friendly version of the post title.

    Args:
        slug: URL-friendly blog post slug (e.g., "building-ai-chatbot-with-strands")

    Returns:
        Complete blog post with title, content, author, published date, tags, and metadata
    """
    post = content_service.get_blog_post(slug)
    if not post:
        return {"error": f"Blog post with slug '{slug}' not found"}
    return post


@tool
def list_recent_blog_posts(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get recent published blog posts.

    Use this tool when users ask about latest blog posts, recent articles, or want to see
    what's new on the blog. Returns the most recently published posts.

    Args:
        limit: Maximum number of posts to return (default: 5, max recommended: 10)

    Returns:
        List of recent blog posts ordered by published date (newest first)
    """
    # Cap limit to prevent excessive results
    limit = min(limit, 10)
    return content_service.list_recent_blog_posts(limit)


@tool
def get_blog_posts_by_tag(tag: str) -> List[Dict[str, Any]]:
    """
    Filter blog posts by tag.

    Use this tool when users want to see all posts about a specific topic or category.
    Tags are typically topics like "AI", "Python", "AWS", "Tutorial", etc.

    Args:
        tag: Tag to filter by (e.g., "AI", "Python", "Tutorial")

    Returns:
        List of blog posts with the specified tag
    """
    return content_service.get_blog_posts_by_tag(tag)

