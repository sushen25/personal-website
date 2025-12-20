from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class BlogPost(BaseModel):
    """Blog post model."""
    postId: str = Field(..., description="Unique post identifier")
    thumbnail: str = Field(..., description="Image url of the thumbnail image")
    title: str = Field(..., description="Post title")
    html_content: str = Field(..., description="Post content in html")
    text_content: str = Field(..., description="Post content in text")
    excerpt: Optional[str] = Field(None, description="Short excerpt")
    created_date: str = Field(..., description="Created date (ISO format)")
    published_date: str = Field(..., description="Publication date (ISO format)")
    status: str = Field("draft", description="Post status: draft, published, archived")
    tags: List[str] = Field(default_factory=list, description="Post tags")
    view_count: int = Field(0, description="Number of views")
    seo_metadata: Optional[Dict[str, str]] = Field(None, description="SEO metadata")


class BlogPostSummary(BaseModel):
    """Blog post summary (without full content)."""
    postId: str
    thumbnail: str = Field(..., description="Image url of the thumbnail image")
    slug: str
    title: str
    excerpt: Optional[str] = None
    created_date: str
    published_date: str
    tags: List[str] = Field(default_factory=list)
    view_count: int = 0
