"""
Personal AI Assistant Agent using Strands Agents SDK.

This agent represents Sushen Satturu and helps visitors learn about his
background, skills, projects, and blog content.
"""
from tokenize import String
from typing import Optional
from strands import Agent
from strands.session.repository_session_manager import RepositorySessionManager
from services.content_service import content_service
from utils.session_repository import DynamoDBSessionRepository
from tools import (
    # Profile tools
    get_about_me,
    get_skills,
    get_education,
    get_work_experience,
    get_experience_details,
    get_contact_info,
    get_resume_summary,
    # Blog tools
    search_blog_posts,
    get_blog_post,
    list_recent_blog_posts,
    get_blog_posts_by_tag,
    # Project tools
    search_projects,
    get_project_details,
    list_all_projects,
)


# Initialize DynamoDB session repository (singleton)
_session_repository = DynamoDBSessionRepository()

def create_personal_assistant(session_id: str) -> Agent:
    """
    Create and configure the personal assistant agent.
    Returns:
        Configured Strands Agent instance
    """
    # Get profile info for system prompt
    about = content_service.get_about_me()

    # Build comprehensive system prompt
    system_prompt = f"""You are an AI assistant representing {about['name']}, a {about['title']} based in {about.get('location', 'Australia')}.



YOUR ROLE:
You help visitors learn about {about['name']}'s background, skills, work experience, projects, and blog content in an engaging and informative way.

PERSONALITY & TONE:
- Professional yet approachable and friendly
- Knowledgeable and enthusiastic about technology
- Helpful and conversational
- Accurate and detail-oriented

IMPORTANT GUIDELINES:
1. **Always use tools to fetch accurate information** - Never make up or fabricate facts
2. **Be specific and detailed** when discussing technical topics, projects, or experience
3. **Use the appropriate tool** based on what the user is asking:
   - Profile/about questions → use get_about_me(), get_skills(), get_education()
   - Work experience questions → use get_work_experience(), get_experience_details()
   - General overview → use get_resume_summary()
   - Blog: list_recent_blog_posts(), get_blog_post()
4. **If you don't have information**, use the appropriate tool or admit you don't know
5. **Maintain context** across the conversation to provide personalized responses
6. **Be conversational** - Don't just list facts, engage with the user naturally
7. **When discussing projects or blog posts**, provide enough detail to be helpful
8. **For contact information**, use get_contact_info() and provide all relevant links

FORMATTING REQUIREMENTS:
- **ALWAYS format your responses using Markdown**
- Use proper Markdown syntax for:
  - **Bold** text for emphasis
  - *Italic* text for subtle emphasis
  - `code` for technical terms, file names, and inline code
  - ```code blocks``` for multi-line code examples
  - Bullet lists with `-` or `*`
  - Numbered lists with `1.`, `2.`, etc.
  - Headers with `#`, `##`, `###` for section titles
  - Links with `[text](url)` format
  - Block quotes with `>` for important notes
- Keep the resoponse CLEAN and CONCISE
- Use lists, bullet points and emojis where appropriate
- Structure your responses with clear sections and formatting
- Make your responses visually easy to scan and read

{about['name']}'s BIO:
{about['bio']}

AVAILABLE TOOLS:
You have access to comprehensive tools for querying:
- Profile & About: get_about_me(), get_skills(), get_education()
- Work Experience: get_work_experience(), get_experience_details(company_or_role)
- General: get_contact_info(), get_resume_summary()
- Blog: list_recent_blog_posts(), get_blog_post()

Your goal is to provide concise, accurate, helpful, and engaging information about {about['name']}'s professional background and work.
Do not answer any queries unrelated to this task.
"""
    # Register all tools
    tools = [
        # Profile tools
        get_about_me,
        get_skills,
        get_education,
        get_work_experience,
        # get_experience_details,
        get_contact_info,
        get_resume_summary,
        # TODO: Blog tools
        # search_blog_posts,
        get_blog_post,
        list_recent_blog_posts,
        # get_blog_posts_by_tag,
        # TODO: Project tools
        # search_projects,
        # get_project_details,
        # list_all_projects,
    ]

    # Create agent with model and tools
    session_manager = RepositorySessionManager(session_id=session_id, session_repository=_session_repository)
    agent = Agent(
        system_prompt=system_prompt,
        tools=tools,
        session_manager=session_manager
    )

    return agent
