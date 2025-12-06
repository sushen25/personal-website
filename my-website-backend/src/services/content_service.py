"""
Content service for formatting and retrieving portfolio content.
This service provides data for the Strands Agent tools.
"""

from typing import List, Dict, Any, Optional
from boto3.dynamodb.conditions import Attr
from src.utils.dynamodb import blog_db


class ContentService:
    """Service for managing and formatting portfolio content."""

    @staticmethod
    def get_about_me() -> Dict[str, Any]:
        """
        Get about me / profile information.

        Returns:
            Dictionary with profile information
        """
        # This will be migrated to DynamoDB in Phase 4
        # For now, return hardcoded data
        return {
            "name": "Sushen Satturu",
            "title": "Software Engineer",
            "bio": "Passionate software engineer with expertise in full-stack development, AI/ML, and cloud technologies.",
            "location": "Australia",
            "email": "contact@sushensatturu.com",
            "linkedin": "https://linkedin.com/in/sushensatturu",
            "github": "https://github.com/sushen25",
            "website": "https://sushensatturu.com"
        }

    @staticmethod
    def get_skills() -> List[Dict[str, str]]:
        """
        Get technical skills.

        Returns:
            List of skills with categories
        """
        # This will be migrated to DynamoDB in Phase 4
        return [
            {"name": "Python", "category": "Programming Languages", "proficiency": "Expert"},
            {"name": "TypeScript", "category": "Programming Languages", "proficiency": "Advanced"},
            {"name": "JavaScript", "category": "Programming Languages", "proficiency": "Advanced"},
            {"name": "React", "category": "Frameworks", "proficiency": "Advanced"},
            {"name": "Next.js", "category": "Frameworks", "proficiency": "Advanced"},
            {"name": "FastAPI", "category": "Frameworks", "proficiency": "Advanced"},
            {"name": "AWS", "category": "Cloud Platforms", "proficiency": "Advanced"},
            {"name": "Docker", "category": "Tools", "proficiency": "Advanced"},
            {"name": "Git", "category": "Tools", "proficiency": "Expert"},
        ]

    @staticmethod
    def get_education() -> List[Dict[str, Any]]:
        """
        Get education history.

        Returns:
            List of education entries
        """
        # This will be migrated to DynamoDB in Phase 4
        return [
            {
                "institution": "University Name",
                "degree": "Bachelor of Science",
                "field_of_study": "Computer Science",
                "start_date": "2015",
                "end_date": "2019",
                "honors": ["Dean's List", "Honors Graduate"]
            }
        ]

    @staticmethod
    def get_work_experience() -> List[Dict[str, Any]]:
        """
        Get complete work history.

        Returns:
            List of work experience entries
        """
        # This will be migrated to DynamoDB in Phase 4
        return [
            {
                "company": "Tech Company",
                "role": "Senior Software Engineer",
                "start_date": "2022-01",
                "end_date": None,  # Current position
                "description": "Leading development of cloud-native applications",
                "technologies": ["Python", "AWS", "React", "TypeScript"],
                "achievements": [
                    "Architected and deployed serverless backend handling 1M+ requests/month",
                    "Reduced infrastructure costs by 40% through optimization"
                ]
            },
            {
                "company": "Previous Company",
                "role": "Software Engineer",
                "start_date": "2019-06",
                "end_date": "2021-12",
                "description": "Full-stack development of web applications",
                "technologies": ["JavaScript", "Node.js", "React", "MongoDB"],
                "achievements": [
                    "Developed e-commerce platform serving 50K+ users",
                    "Implemented CI/CD pipeline reducing deployment time by 60%"
                ]
            }
        ]

    @staticmethod
    def get_experience_details(company_or_role: str) -> Optional[Dict[str, Any]]:
        """
        Get details about a specific role or company.

        Args:
            company_or_role: Company name or role title to search for

        Returns:
            Experience details or None if not found
        """
        experiences = ContentService.get_work_experience()
        search_term = company_or_role.lower()

        for exp in experiences:
            if search_term in exp['company'].lower() or search_term in exp['role'].lower():
                return exp

        return None

    @staticmethod
    def list_all_projects() -> List[Dict[str, Any]]:
        """
        Get all projects with summaries.

        Returns:
            List of project summaries
        """
        # This will be migrated to DynamoDB in Phase 4
        return [
            {
                "project_id": "1",
                "name": "Portfolio Website",
                "description": "Personal portfolio with AI chatbot powered by Strands Agents",
                "technologies": ["Python", "FastAPI", "Next.js", "AWS Lambda", "Strands Agents"],
                "github_url": "https://github.com/sushen25/portfolio",
                "demo_url": "https://sushensatturu.com",
                "status": "in-progress"
            },
            {
                "project_id": "2",
                "name": "Task Management System",
                "description": "Full-stack task management application with real-time collaboration",
                "technologies": ["React", "Node.js", "MongoDB", "WebSockets"],
                "github_url": "https://github.com/sushen25/task-manager",
                "status": "completed"
            }
        ]

    @staticmethod
    def search_projects(query: str) -> List[Dict[str, Any]]:
        """
        Search projects by keyword, technology, or type.

        Args:
            query: Search query string

        Returns:
            List of matching projects
        """
        all_projects = ContentService.list_all_projects()
        query_lower = query.lower()

        matching_projects = []
        for project in all_projects:
            # Search in name, description, and technologies
            if (query_lower in project['name'].lower() or
                query_lower in project['description'].lower() or
                any(query_lower in tech.lower() for tech in project['technologies'])):
                matching_projects.append(project)

        return matching_projects

    @staticmethod
    def get_project_details(project_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific project.

        Args:
            project_name: Name of the project

        Returns:
            Project details or None if not found
        """
        all_projects = ContentService.list_all_projects()
        name_lower = project_name.lower()

        for project in all_projects:
            if name_lower in project['name'].lower():
                return project

        return None

    @staticmethod
    def search_blog_posts(query: str) -> List[Dict[str, Any]]:
        """
        Search blog posts by title, tags, or content.

        Args:
            query: Search query string

        Returns:
            List of matching blog posts
        """
        # Query DynamoDB for published blog posts
        # This assumes blog posts will be in DynamoDB
        # For now, return empty list until Phase 4 migration
        return []

    @staticmethod
    def get_blog_post(slug: str) -> Optional[Dict[str, Any]]:
        """
        Fetch full blog post by slug.

        Args:
            slug: URL-friendly blog post slug

        Returns:
            Blog post details or None if not found
        """
        # This will query DynamoDB once blog posts are migrated
        return None

    @staticmethod
    def list_recent_blog_posts(limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get recent published blog posts.

        Args:
            limit: Maximum number of posts to return

        Returns:
            List of recent blog posts
        """
        # This will query DynamoDB once blog posts are migrated
        # For now, return placeholder data
        return [
            {
                "post_id": "1",
                "slug": "building-ai-chatbot-with-strands",
                "title": "Building an AI Chatbot with Strands Agents",
                "excerpt": "Learn how to build a production-ready AI chatbot using AWS Strands Agents framework",
                "published_date": "2025-01-15",
                "tags": ["AI", "Python", "AWS", "Strands Agents"]
            }
        ]

    @staticmethod
    def get_blog_posts_by_tag(tag: str) -> List[Dict[str, Any]]:
        """
        Filter blog posts by tag.

        Args:
            tag: Tag to filter by

        Returns:
            List of blog posts with the specified tag
        """
        # This will query DynamoDB with tag filter
        return []

    @staticmethod
    def get_contact_info() -> Dict[str, str]:
        """
        Return contact methods.

        Returns:
            Dictionary with contact information
        """
        about = ContentService.get_about_me()
        return {
            "email": about.get("email", ""),
            "linkedin": about.get("linkedin", ""),
            "github": about.get("github", ""),
            "website": about.get("website", "")
        }

    @staticmethod
    def get_resume_summary() -> str:
        """
        Generate comprehensive profile summary.

        Returns:
            Formatted resume summary string
        """
        about = ContentService.get_about_me()
        experience = ContentService.get_work_experience()
        education = ContentService.get_education()
        skills = ContentService.get_skills()

        summary = f"""
{about['name']} - {about['title']}
{about['bio']}

Location: {about.get('location', 'N/A')}

Work Experience:
"""
        for exp in experience:
            end = exp['end_date'] or 'Present'
            summary += f"\n{exp['role']} at {exp['company']} ({exp['start_date']} - {end})"
            summary += f"\n{exp['description']}"

        summary += "\n\nEducation:\n"
        for edu in education:
            summary += f"{edu['degree']} in {edu['field_of_study']} from {edu['institution']}\n"

        summary += "\nKey Skills:\n"
        for skill in skills[:10]:  # Top 10 skills
            summary += f"- {skill['name']} ({skill['category']})\n"

        return summary.strip()

    @staticmethod
    def format_for_chatbot() -> str:
        """
        Format all content as a comprehensive system prompt for the chatbot.

        Returns:
            Formatted system prompt string
        """
        about = ContentService.get_about_me()

        prompt = f"""You are an AI assistant representing {about['name']}, a {about['title']}.

ABOUT:
{about['bio']}

You have access to tools to query detailed information about:
- Profile and skills
- Work experience and career history
- Projects and portfolio
- Blog posts and articles
- Contact information

IMPORTANT GUIDELINES:
1. Use the available tools to fetch accurate, up-to-date information
2. Never make up or fabricate information - always use tools to verify
3. Be professional yet approachable in your responses
4. When discussing technical topics, be specific and detailed
5. If you don't have information, use the appropriate tool or admit you don't know
6. Maintain context across conversations to provide helpful, personalized responses

Your goal is to help visitors learn about {about['name']}'s background, skills, projects, and content in an engaging and informative way.
"""
        return prompt.strip()


# Global instance for reuse
content_service = ContentService()
