"""
Content service for retrieving portfolio content from DynamoDB.
This service provides data for the Strands Agent tools.
"""

from typing import List, Dict, Any, Optional
from boto3.dynamodb.conditions import Key, Attr
from utils.dynamodb import blog_db
from portfolio_common.services.blog_service import BlogService
import asyncio


class ContentService:
    """Service for managing and retrieving portfolio content from DynamoDB."""

    # Initialize shared blog service
    _blog_service = BlogService(blog_db)

    @staticmethod
    def get_about_me() -> Dict[str, Any]:
        """
        Get about me / profile information.

        Returns:
            Dictionary with profile information
        """
        return {
            "name": "Sushen Satturu",
            "title": "Software Engineer",
            "bio": "I'm a full-stack software engineer with a strong focus on building scalable web applications and cloud infrastructure, mostly in fast-moving startup environments. I've worked across the stack—frontend, backend, and DevOps—and enjoy taking ownership of features from idea through to production. At TeamAssurance, I've led projects used by global clients like CSL and Suntory, and helped shape core parts of the product. I'm particularly interested in how AI and machine learning can be applied to solve real-world problems, and have been experimenting with LLMs and smart integrations into existing platforms.",
            "location": "Melbourne, VIC 3030, Australia",
            "phone": "+61 40 678 6789",
            "email": "sushensatturu25@gmail.com",
            "linkedin": "https://linkedin.com/in/sushen-satturu-646403182",
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
        return [
            {"name": "React", "category": "Frontend", "proficiency": "Advanced"},
            {"name": "Node.js", "category": "Backend", "proficiency": "Advanced"},
            {"name": "MySQL", "category": "Databases", "proficiency": "Advanced"},
            {"name": "PostgreSQL", "category": "Databases", "proficiency": "Advanced"},
            {"name": "MongoDB", "category": "Databases", "proficiency": "Advanced"},
            {"name": "Cassandra", "category": "Databases", "proficiency": "Intermediate"},
            {"name": "Neo4J", "category": "Databases", "proficiency": "Intermediate"},
            {"name": "AWS", "category": "Cloud & Infrastructure", "proficiency": "Advanced"},
            {"name": "Application Integrations", "category": "Integration & APIs", "proficiency": "Advanced"},
            {"name": "Webhooks", "category": "Integration & APIs", "proficiency": "Advanced"},
            {"name": "IoT Devices", "category": "Integration & APIs", "proficiency": "Intermediate"},
            {"name": "LLM Development", "category": "AI/ML", "proficiency": "Advanced"},
            {"name": "AI", "category": "AI/ML", "proficiency": "Advanced"},
            {"name": "Machine Learning", "category": "AI/ML", "proficiency": "Intermediate"},
            {"name": "Requirements Gathering", "category": "Soft Skills", "proficiency": "Advanced"},
            {"name": "Client Communication", "category": "Soft Skills", "proficiency": "Advanced"},
        ]

    @staticmethod
    def get_education() -> List[Dict[str, Any]]:
        """
        Get education history.

        Returns:
            List of education entries
        """
        return [
            {
                "institution": "University",
                "degree": "Bachelor of Computer Science",
                "field_of_study": "Computer Science",
                "start_date": "2018",
                "end_date": "2021",
                "honors": ["Graduated with honors"],
                "coursework": [
                    "Data Structures and Algorithms",
                    "Web Development",
                    "Database Systems"
                ]
            },
            {
                "institution": "University",
                "degree": "Bachelor of Commerce",
                "field_of_study": "Commerce",
                "start_date": "2018",
                "end_date": "2021",
                "coursework": [
                    "Finance",
                    "Economics",
                    "Business Law",
                    "Marketing"
                ]
            }
        ]

    @staticmethod
    def get_work_experience() -> List[Dict[str, Any]]:
        """
        Get complete work history.

        Returns:
            List of work experience entries
        """
        return [
            {
                "company": "TeamAssurance",
                "role": "Software Engineer",
                "start_date": "2024",
                "end_date": None,  # Current position
                "description": "Full-stack development in a fast-paced startup environment, working with global clients including CSL, Suntory, and Pact.",
                "technologies": ["React", "Node.js", "AWS", "Full-Stack"],
                "achievements": [
                    "Develop and maintain full-stack applications in a fast-paced startup environment",
                    "Design and implement cloud infrastructure solutions using AWS",
                    "Collaborate with global clients including CSL, Suntory, and Pact",
                    "Lead cross-functional development across UI, backend, and DevOps domains",
                    "Led projects used by global clients and helped shape core parts of the product"
                ]
            },
            {
                "company": "WSP",
                "role": "Software Engineer",
                "start_date": "2021",
                "end_date": "2024",
                "description": "Delivered end-to-end software solutions for major clients, including the Australian Defence Force and Transport New South Wales.",
                "technologies": ["Full-Stack", "Agile", "DevOps"],
                "achievements": [
                    "Delivered end-to-end software solutions for major clients, including the Australian Defence Force and Transport New South Wales",
                    "Led technical mentorship program for interns and junior developers",
                    "Ensured high-quality project delivery within strict timelines and requirements",
                    "Implemented agile development methodologies to optimize team productivity"
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
                any(query_lower in tech.lower() for tech in project.get('technologies', []))):
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
        try:
            query_lower = query.lower()

            # Get all published posts using shared BlogService
            posts = asyncio.run(ContentService._blog_service.list_posts(status='published', limit=50))

            # Convert BlogPostSummary objects to dicts and filter by query term
            matching_posts = []
            for post in posts:
                post_dict = post.model_dump()
                # Search in title, excerpt, tags
                if (query_lower in post_dict.get('title', '').lower() or
                    query_lower in post_dict.get('excerpt', '').lower() or
                    any(query_lower in tag.lower() for tag in post_dict.get('tags', []))):
                    matching_posts.append(post_dict)

            return matching_posts
        except Exception as e:
            print(f"Error searching blog posts: {str(e)}")
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
        try:
            post = asyncio.run(ContentService._blog_service.get_post_by_slug(slug))
            return post.model_dump() if post else None
        except Exception as e:
            print(f"Error getting blog post: {str(e)}")
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
        try:
            posts = asyncio.run(ContentService._blog_service.list_posts(status='published', limit=limit))
            return [post.model_dump() for post in posts]
        except Exception as e:
            print(f"Error listing recent blog posts: {str(e)}")
            return []

    @staticmethod
    def get_blog_posts_by_tag(tag: str) -> List[Dict[str, Any]]:
        """
        Filter blog posts by tag.

        Args:
            tag: Tag to filter by

        Returns:
            List of blog posts with the specified tag
        """
        try:
            # Get all published posts and filter by tag
            posts = asyncio.run(ContentService._blog_service.list_posts(status='published', limit=50))
            matching_posts = [
                post.model_dump()
                for post in posts
                if tag in post.tags
            ]
            return matching_posts
        except Exception as e:
            print(f"Error getting blog posts by tag: {str(e)}")
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
            "website": about.get("website", ""),
            "preferred_contact": "Email or LinkedIn"
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
Website: {about['website']}
GitHub: {about['github']}
LinkedIn: {about['linkedin']}

WORK EXPERIENCE
"""
        for exp in experience:
            end = exp['end_date'] or 'Present'
            summary += f"\n{exp['role']} at {exp['company']} ({exp['start_date']} - {end})"
            summary += f"\n{exp['description']}"
            if exp.get('technologies'):
                summary += f"\nTechnologies: {', '.join(exp['technologies'])}"
            if exp.get('achievements'):
                summary += "\nKey Achievements:"
                for achievement in exp['achievements']:
                    summary += f"\n  • {achievement}"
            summary += "\n"

        summary += "\nEDUCATION\n"
        for edu in education:
            summary += f"\n{edu['degree']} in {edu['field_of_study']}"
            summary += f"\n{edu['institution']} ({edu['start_date']} - {edu['end_date']})"
            if edu.get('gpa'):
                summary += f"\nGPA: {edu['gpa']}"
            if edu.get('honors'):
                summary += f"\nHonors: {', '.join(edu['honors'])}"
            summary += "\n"

        summary += "\nTOP SKILLS\n"
        # Group skills by category
        skills_by_category = {}
        for skill in skills:
            category = skill['category']
            if category not in skills_by_category:
                skills_by_category[category] = []
            skills_by_category[category].append(f"{skill['name']} ({skill['proficiency']})")

        for category, skill_list in skills_by_category.items():
            summary += f"\n{category}:\n"
            for skill_name in skill_list:
                summary += f"  • {skill_name}\n"

        return summary.strip()


# Global instance for reuse
content_service = ContentService()

