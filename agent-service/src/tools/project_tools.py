"""
Custom tools for project queries.
"""

from strands import tool
from typing import List, Dict, Any, Optional
from services.content_service import content_service


@tool
def search_projects(query: str) -> List[Dict[str, Any]]:
    """
    Search projects by keyword, technology, or type.

    Use this tool when users ask about projects that use specific technologies, work on
    certain topics, or want to find projects matching a description. The search looks
    through project names, descriptions, and technologies.

    Args:
        query: Search query string (e.g., "Python", "React", "AI", "web app")

    Returns:
        List of matching projects with name, description, technologies, and links
    """
    return content_service.search_projects(query)


@tool
def get_project_details(project_name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific project.

    Use this tool when users ask about a specific project by name or want detailed
    information about a particular project. This returns comprehensive project details
    including description, technologies, links, and status.

    Args:
        project_name: Name of the project (e.g., "Portfolio Website", "Task Management System")

    Returns:
        Complete project details including description, technologies, GitHub URL, demo URL, and status
    """
    project = content_service.get_project_details(project_name)
    if not project:
        return {"error": f"Project '{project_name}' not found"}
    return project


@tool
def list_all_projects() -> List[Dict[str, Any]]:
    """
    Return all projects with summaries.

    Use this tool when users ask to see all projects, want an overview of the portfolio,
    or ask "what projects have you worked on". Returns a comprehensive list of all projects.

    Returns:
        List of all projects with name, description, technologies, and status
    """
    return content_service.list_all_projects()

