"""
Content service for retrieving portfolio content from DynamoDB.
This service provides data for the Strands Agent tools.
"""

from typing import List, Dict, Any, Optional
from boto3.dynamodb.conditions import Key, Attr
from src.utils.dynamodb import blog_db


class ContentService:
    """Service for managing and retrieving portfolio content from DynamoDB."""

    @staticmethod
    def get_about_me() -> Dict[str, Any]:
        """
        Get about me / profile information.

        Returns:
            Dictionary with profile information
        """
        # TODO: Query DynamoDB once content is migrated (Phase 4)
        # For now, return hardcoded data
        return {
            "name": "Sushen Satturu",
            "title": "Software Engineer",
            "bio": "Passionate software engineer with expertise in full-stack development, AI/ML, and cloud technologies. Specializing in building scalable serverless applications and intelligent systems using modern frameworks and AWS services.",
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
        # TODO: Query DynamoDB once content is migrated (Phase 4)
        return [
            {"name": "Python", "category": "Programming Languages", "proficiency": "Expert"},
            {"name": "TypeScript", "category": "Programming Languages", "proficiency": "Advanced"},
            {"name": "JavaScript", "category": "Programming Languages", "proficiency": "Advanced"},
            {"name": "Java", "category": "Programming Languages", "proficiency": "Intermediate"},
            {"name": "React", "category": "Frontend Frameworks", "proficiency": "Advanced"},
            {"name": "Next.js", "category": "Frontend Frameworks", "proficiency": "Advanced"},
            {"name": "Vue.js", "category": "Frontend Frameworks", "proficiency": "Intermediate"},
            {"name": "FastAPI", "category": "Backend Frameworks", "proficiency": "Advanced"},
            {"name": "Express.js", "category": "Backend Frameworks", "proficiency": "Advanced"},
            {"name": "Node.js", "category": "Backend Frameworks", "proficiency": "Advanced"},
            {"name": "AWS", "category": "Cloud Platforms", "proficiency": "Advanced"},
            {"name": "Lambda", "category": "Cloud Platforms", "proficiency": "Advanced"},
            {"name": "DynamoDB", "category": "Cloud Platforms", "proficiency": "Advanced"},
            {"name": "API Gateway", "category": "Cloud Platforms", "proficiency": "Advanced"},
            {"name": "Strands Agents", "category": "AI/ML", "proficiency": "Advanced"},
            {"name": "OpenAI API", "category": "AI/ML", "proficiency": "Advanced"},
            {"name": "LangChain", "category": "AI/ML", "proficiency": "Intermediate"},
            {"name": "Docker", "category": "DevOps Tools", "proficiency": "Advanced"},
            {"name": "Git", "category": "DevOps Tools", "proficiency": "Expert"},
            {"name": "Serverless Framework", "category": "DevOps Tools", "proficiency": "Advanced"},
            {"name": "CI/CD", "category": "DevOps Tools", "proficiency": "Advanced"},
        ]

    @staticmethod
    def get_education() -> List[Dict[str, Any]]:
        """
        Get education history.

        Returns:
            List of education entries
        """
        # TODO: Query DynamoDB once content is migrated (Phase 4)
        return [
            {
                "institution": "University Name",
                "degree": "Bachelor of Science",
                "field_of_study": "Computer Science",
                "start_date": "2015",
                "end_date": "2019",
                "gpa": "3.8/4.0",
                "honors": [
                    "Dean's List",
                    "Honors Graduate",
                    "Computer Science Achievement Award"
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
        # TODO: Query DynamoDB once content is migrated (Phase 4)
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
        # TODO: Query DynamoDB once content is migrated (Phase 4)
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
            # Query DynamoDB for published blog posts
            # Use GSI StatusPublishedDateIndex to get published posts
            query_lower = query.lower()
            
            # First, get all published posts
            items = blog_db.query(
                key_condition=Key('status').eq('published'),
                index_name='StatusPublishedDateIndex',
                limit=50
            )
            
            # Filter by query term
            matching_posts = []
            for post in items:
                # Search in title, excerpt, tags, and content
                if (query_lower in post.get('title', '').lower() or
                    query_lower in post.get('excerpt', '').lower() or
                    query_lower in post.get('content', '').lower() or
                    any(query_lower in tag.lower() for tag in post.get('tags', []))):
                    matching_posts.append(post)
            
            return matching_posts
        except Exception as e:
            print(f"Error searching blog posts: {str(e)}")
            # Fallback to empty list if DynamoDB query fails
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
            # Query DynamoDB using SlugIndex GSI
            items = blog_db.query(
                key_condition=Key('slug').eq(slug),
                index_name='SlugIndex',
                limit=1
            )
            
            if items:
                return items[0]
            return None
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
            # Query DynamoDB using StatusPublishedDateIndex, sorted by publishedDate descending
            items = blog_db.query(
                key_condition=Key('status').eq('published'),
                index_name='StatusPublishedDateIndex',
                limit=limit,
                scan_index_forward=False  # Descending order (most recent first)
            )
            
            return items
        except Exception as e:
            print(f"Error listing recent blog posts: {str(e)}")
            # Fallback to empty list if DynamoDB query fails
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
            items = blog_db.query(
                key_condition=Key('status').eq('published'),
                index_name='StatusPublishedDateIndex',
                filter_expression=Attr('tags').contains(tag),
                limit=50
            )
            
            return items
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

