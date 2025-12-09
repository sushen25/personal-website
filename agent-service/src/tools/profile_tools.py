"""
Custom tools for profile, skills, and education queries.
"""

from strands import tool
from typing import List, Dict, Any, Optional
from services.content_service import content_service


@tool
def get_about_me() -> Dict[str, Any]:
    """
    Get comprehensive profile and about information for Sushen Satturu.

    Returns detailed bio, current role, location, and contact information.
    Use this tool when users ask about background, who you are, or general profile info.

    Returns:
        Dictionary with name, title, bio, location, and contact links
    """
    return content_service.get_about_me()


@tool
def get_skills() -> List[Dict[str, str]]:
    """
    Get comprehensive list of technical skills organized by category.

    Returns skills in programming languages, frameworks, cloud platforms, and tools.
    Use this when users ask about technical skills, expertise, or technologies known.

    Returns:
        List of skill dictionaries with name, category, and proficiency level
    """
    return content_service.get_skills()


@tool
def get_education() -> List[Dict[str, Any]]:
    """
    Get education history including degrees, institutions, and honors.

    Returns all formal education credentials and achievements.
    Use this when users ask about educational background or qualifications.

    Returns:
        List of education entries with institution, degree, field, dates, and honors
    """
    return content_service.get_education()


@tool
def get_work_experience() -> List[Dict[str, Any]]:
    """
    Get complete work history and professional experience.

    Returns all work experience entries with company, role, dates, descriptions,
    technologies, and achievements. Use this when users ask about work history,
    previous jobs, or career experience.

    Returns:
        List of work experience entries with comprehensive details
    """
    return content_service.get_work_experience()


@tool
def get_experience_details(company_or_role: str) -> Dict[str, Any]:
    """
    Get details about a specific role or company.

    Use this tool when users ask about a specific job, company, or role.
    Searches through work history to find matching experience.

    Args:
        company_or_role: Company name or role title to search for (e.g., "Tech Company", "Senior Software Engineer")

    Returns:
        Experience details or error message if not found
    """
    experience = content_service.get_experience_details(company_or_role)
    if not experience:
        return {"error": f"Experience matching '{company_or_role}' not found"}
    return experience


@tool
def get_contact_info() -> Dict[str, str]:
    """
    Get all contact methods and professional profile links.

    Returns email, LinkedIn, GitHub, and website URLs.
    Use this when users want to connect or reach out.

    Returns:
        Dictionary with contact methods and links
    """
    return content_service.get_contact_info()


@tool
def get_resume_summary() -> str:
    """
    Generate a comprehensive resume-style summary combining all profile information.

    Returns formatted text with complete professional profile including experience,
    education, and skills. Use this for general overview or resume requests.

    Returns:
        Formatted resume summary as string
    """
    return content_service.get_resume_summary()
