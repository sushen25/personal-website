"""
Pydantic models for request/response validation.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


# Chat Models
class ChatMessage(BaseModel):
    """Single chat message model."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[float] = Field(None, description="Unix timestamp")


class ChatRequest(BaseModel):
    """Chat request model."""
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    messages: List[ChatMessage] = Field(..., description="List of chat messages")
    model_provider: Optional[str] = Field(None, description="AI model provider (bedrock, openai, anthropic)")

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "messages": [
                    {"role": "user", "content": "What's your latest blog post?"}
                ],
                "model_provider": "bedrock"
            }
        }


class ChatResponse(BaseModel):
    """Chat response model."""
    session_id: str = Field(..., description="Session ID for this conversation")
    message: ChatMessage = Field(..., description="Assistant's response message")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "550e8400-e29b-41d4-a716-446655440000",
                "message": {
                    "role": "assistant",
                    "content": "My latest blog post is about...",
                    "timestamp": 1234567890.0
                },
                "metadata": {
                    "model_used": "bedrock/claude-3-5-sonnet",
                    "token_count": 150,
                    "response_time_ms": 1200
                }
            }
        }


class ConversationHistory(BaseModel):
    """Conversation history model."""
    session_id: str = Field(..., description="Session ID")
    messages: List[ChatMessage] = Field(..., description="List of messages in chronological order")
    created_at: Optional[datetime] = Field(None, description="Conversation start time")
    updated_at: Optional[datetime] = Field(None, description="Last message time")


# Blog Models
class BlogPost(BaseModel):
    """Blog post model."""
    post_id: str = Field(..., description="Unique post identifier")
    slug: str = Field(..., description="URL-friendly slug")
    title: str = Field(..., description="Post title")
    content: str = Field(..., description="Post content (markdown)")
    excerpt: Optional[str] = Field(None, description="Short excerpt")
    author: str = Field(..., description="Author name")
    published_date: str = Field(..., description="Publication date (ISO format)")
    status: str = Field("draft", description="Post status: draft, published, archived")
    tags: List[str] = Field(default_factory=list, description="Post tags")
    view_count: int = Field(0, description="Number of views")
    seo_metadata: Optional[Dict[str, str]] = Field(None, description="SEO metadata")


class BlogPostSummary(BaseModel):
    """Blog post summary (without full content)."""
    post_id: str
    slug: str
    title: str
    excerpt: Optional[str] = None
    published_date: str
    tags: List[str] = Field(default_factory=list)
    view_count: int = 0


# Analytics Models
class AnalyticsEvent(BaseModel):
    """Analytics event model."""
    event_id: str = Field(..., description="Unique event identifier")
    metric_type: str = Field(..., description="Event type: pageview, chatInteraction, apiCall, error")
    timestamp: float = Field(..., description="Unix timestamp")
    data: Dict[str, Any] = Field(..., description="Event data")
    ttl: Optional[int] = Field(None, description="TTL for auto-deletion")


# Portfolio/Profile Models
class AboutMe(BaseModel):
    """About me / profile information."""
    name: str
    title: str
    bio: str
    location: Optional[str] = None
    email: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None


class Skill(BaseModel):
    """Technical skill model."""
    name: str
    category: str  # e.g., "Programming Languages", "Frameworks", "Tools"
    proficiency: Optional[str] = None  # e.g., "Expert", "Advanced", "Intermediate"


class WorkExperience(BaseModel):
    """Work experience entry."""
    company: str
    role: str
    start_date: str
    end_date: Optional[str] = None  # None for current position
    description: str
    technologies: List[str] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)


class Education(BaseModel):
    """Education entry."""
    institution: str
    degree: str
    field_of_study: str
    start_date: str
    end_date: Optional[str] = None
    gpa: Optional[str] = None
    honors: List[str] = Field(default_factory=list)


class Project(BaseModel):
    """Project model."""
    project_id: str
    name: str
    description: str
    technologies: List[str]
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    image_url: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: str = "completed"  # completed, in-progress, archived


# Error Models
class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
    detail: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
