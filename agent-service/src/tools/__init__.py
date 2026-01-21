"""
Custom tools for the personal assistant agent.
All tools are exported here for easy import.
"""

# Profile tools
from tools.profile_tools import (
    get_about_me,
    get_skills,
    get_education,
    get_work_experience,
    get_experience_details,
    get_contact_info,
    get_resume_summary,
)

# Blog tools
from tools.blog_tools import (
    search_blog_posts,
    get_blog_post,
    list_recent_blog_posts,
    get_blog_posts_by_tag,
)

# Project tools
from tools.project_tools import (
    search_projects,
    get_project_details,
    list_all_projects,
)

__all__ = [
    # Profile tools
    "get_about_me",
    "get_skills",
    "get_education",
    "get_work_experience",
    "get_experience_details",
    "get_contact_info",
    "get_resume_summary",
    # Blog tools
    "search_blog_posts",
    "get_blog_post",
    "list_recent_blog_posts",
    "get_blog_posts_by_tag",
    # Project tools
    "search_projects",
    "get_project_details",
    "list_all_projects",
]

