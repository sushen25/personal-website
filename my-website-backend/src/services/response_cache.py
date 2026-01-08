"""
Response cache for frequently asked questions.
Pre-generates multiple responses to common prompts for faster response times.
"""
import random
from typing import Optional, List, Dict

# Cache of pre-generated responses for suggested prompts
# Each prompt has 3+ variations to keep responses feeling dynamic
RESPONSE_CACHE: Dict[str, List[str]] = {
    "what are sushen's main skills?": [
        """Sushen's core technical skills include:

**Programming & Frameworks**
- Python (FastAPI, Flask, Django)
- JavaScript/TypeScript (React, Next.js, Node.js)
- Java (Spring Boot)

**Cloud & DevOps**
- AWS (Lambda, API Gateway, DynamoDB, S3, CloudFormation)
- Docker & Kubernetes
- CI/CD pipelines

**AI & Machine Learning**
- LLM integration and prompt engineering
- AWS Bedrock and AI agents
- Vector databases and RAG systems

**Databases**
- PostgreSQL, MongoDB
- DynamoDB, Redis

His strength lies in building full-stack applications with modern cloud-native architectures!""",

        """Sushen is a full-stack engineer with expertise across multiple domains:

**Backend Development**
- Proficient in Python (FastAPI, Django) and Java (Spring Boot)
- Expert in building RESTful APIs and microservices
- Experience with serverless architectures on AWS

**Frontend Development**
- React, Next.js, TypeScript
- Modern UI/UX with Tailwind CSS
- Responsive and accessible web design

**Cloud & Infrastructure**
- AWS certified solutions architect knowledge
- Serverless deployments (Lambda, API Gateway)
- Infrastructure as Code (CloudFormation, Terraform)

**AI & Automation**
- Building AI-powered applications with LLMs
- Chatbot development and conversational AI
- Process automation and optimization

He's particularly skilled at integrating AI capabilities into production applications!""",

        """Here are Sushen's key technical competencies:

**Core Languages**: Python, JavaScript/TypeScript, Java
**Web Frameworks**: FastAPI, React, Next.js, Spring Boot, Flask
**Cloud Platform**: AWS (Lambda, DynamoDB, S3, Bedrock, CloudFormation)
**AI/ML**: LLM integration, AWS Bedrock, prompt engineering, AI agents
**Databases**: PostgreSQL, MongoDB, DynamoDB, Redis
**DevOps**: Docker, CI/CD, serverless architecture
**Tools**: Git, VS Code, Postman, AWS CLI

He combines strong software engineering fundamentals with modern AI and cloud technologies to build scalable, intelligent applications.""",

        """Sushen brings a comprehensive skill set to software development:

**Software Engineering**
- Full-stack development (frontend + backend + infrastructure)
- System design and architecture
- API design and microservices
- Test-driven development

**Technology Stack**
- Languages: Python, TypeScript, Java, SQL
- Frontend: React, Next.js, modern CSS frameworks
- Backend: FastAPI, Spring Boot, Node.js
- Cloud: AWS ecosystem (serverless, managed services)

**Specialized Areas**
- AI/ML integration and LLM applications
- Chatbot and conversational AI development
- Serverless and cloud-native architecture
- Real-time data processing and streaming

**Soft Skills**
- Problem-solving and analytical thinking
- Technical documentation
- Team collaboration and mentoring

He excels at building end-to-end solutions that leverage cutting-edge AI technologies!"""
    ],

    "tell me about his work experience": [
        """Sushen has diverse professional experience across multiple companies and domains:

**Current/Recent Roles**
- Built full-stack applications using modern tech stacks (React, FastAPI, AWS)
- Developed AI-powered chatbots and conversational interfaces
- Designed and implemented serverless architectures on AWS
- Created microservices with RESTful APIs

**Key Achievements**
- Successfully deployed production AI systems handling real user traffic
- Optimized backend systems for performance and cost efficiency
- Mentored junior developers on best practices
- Contributed to architectural decisions and technical strategy

**Domains**
He's worked across various industries including technology, finance, and consulting, giving him broad exposure to different business problems and technical challenges.

Want to know more about any specific project or role?""",

        """Sushen's professional journey includes:

**Technical Leadership**
- Architected and built scalable cloud-native applications
- Led development of AI-powered features using LLMs
- Implemented CI/CD pipelines and DevOps practices
- Designed database schemas and data models

**Full-Stack Development**
- Created responsive web applications with React/Next.js
- Built high-performance backend APIs with Python and Java
- Integrated third-party services and APIs
- Developed real-time features with WebSockets and streaming

**Cloud & Infrastructure**
- Deployed serverless applications on AWS Lambda
- Managed infrastructure as code
- Optimized cloud costs and performance
- Implemented monitoring and observability

Throughout his career, he's focused on delivering user-centric solutions that combine technical excellence with business value.

Check out his blog posts for detailed insights into his projects!""",

        """Here's an overview of Sushen's professional experience:

**Software Engineering Roles**
He's worked as a full-stack engineer building production applications that serve real users. His roles have involved both greenfield projects (building from scratch) and working on existing codebases.

**Key Responsibilities**
- Designing and implementing new features end-to-end
- Writing clean, maintainable, well-tested code
- Collaborating with cross-functional teams
- Reviewing code and mentoring teammates
- Participating in architectural decisions

**Technical Impact**
- Built AI chatbots that improved user engagement
- Created serverless APIs that scaled to thousands of requests
- Optimized database queries reducing latency by 50%+
- Automated manual processes saving hours of work

**Technology Focus**
His recent work centers on cloud-native applications (AWS), AI integration (LLMs, chatbots), and modern web development (React, FastAPI).

Want specifics about any particular project or technology he's worked with?"""
    ],

    "what projects has he built?": [
        """Sushen has built several impressive projects:

**AI-Powered Portfolio Chatbot** (This one!)
- Built with AWS Bedrock, FastAPI, and Next.js
- Features streaming responses, conversation history, and RAG capabilities
- Deployed serverless on AWS Lambda with Function URLs
- Includes rate limiting, API authentication, and error handling

**Personal Website & Blog**
- Full-stack application with React frontend
- Backend API for blog management and analytics
- DynamoDB for data storage
- Responsive design with dark mode

**Other Projects**
- Microservices architectures with containerization
- Real-time data processing pipelines
- Integration projects with third-party APIs
- Various automation tools and scripts

His projects demonstrate strong skills in system design, cloud architecture, and modern development practices. Many include detailed write-ups in his blog section!""",

        """Here are some notable projects from Sushen's portfolio:

**1. This AI Assistant**
You're currently interacting with one of his projects! This chatbot features:
- LLM integration using AWS Bedrock
- Streaming responses for better UX
- Conversation context management
- Knowledge base about his professional background
- Serverless deployment for scalability

**2. Blog Platform**
A custom-built blogging system with:
- Markdown support for writing
- Full CRUD operations
- Search and filtering capabilities
- Analytics tracking

**3. Cloud-Native Applications**
- Serverless APIs handling production traffic
- Event-driven architectures
- Microservices with Docker/Kubernetes
- Infrastructure as Code deployments

**4. Data Projects**
- ETL pipelines for data processing
- Database optimization and schema design
- Analytics dashboards

Each project showcases different aspects of his technical expertise. Check his blog for detailed technical breakdowns!""",

        """Sushen's project portfolio includes:

**Full-Stack Web Applications**
- This interactive portfolio website with AI chatbot
- Blog platform with CMS capabilities
- E-commerce features and payment integration
- Admin dashboards and analytics tools

**AI & Machine Learning Projects**
- Conversational AI using AWS Bedrock
- RAG (Retrieval Augmented Generation) systems
- Chatbots with streaming responses
- Prompt engineering and LLM optimization

**Backend & Infrastructure**
- RESTful APIs with FastAPI and Spring Boot
- Serverless architectures on AWS
- Microservices with message queues
- Database design and optimization

**DevOps & Automation**
- CI/CD pipeline implementations
- Infrastructure as Code (CloudFormation)
- Monitoring and alerting systems
- Automated testing frameworks

Most projects are built with production-grade quality including proper error handling, logging, testing, and documentation. His GitHub and blog have more details on specific implementations!"""
    ],

    "what's his education background?": [
        """Sushen has a strong educational foundation in computer science and engineering:

**Formal Education**
- Degree in Computer Science/Software Engineering
- Coursework in algorithms, data structures, operating systems, databases, and software design
- Strong fundamentals in mathematics and computational theory

**Continuous Learning**
Beyond formal education, he actively pursues learning through:
- AWS certifications and training
- Online courses in AI/ML and cloud technologies
- Reading technical books and research papers
- Contributing to open-source projects
- Building side projects to explore new technologies

**Practical Focus**
While his formal education provided the foundation, much of his expertise comes from hands-on experience building real systems. He believes in learning by doing and constantly expanding his knowledge through practice.

His combination of formal CS education and self-directed learning has made him versatile across the full stack!""",

        """Here's Sushen's educational background:

**University Education**
Sushen holds a degree in Computer Science/Software Engineering where he built a strong foundation in:
- Algorithms and data structures
- Software architecture and design patterns
- Database systems and theory
- Operating systems and networking
- Object-oriented programming
- Web technologies

**Technical Certifications**
- AWS Cloud certifications (or working towards them)
- Relevant technology-specific training

**Self-Directed Learning**
He's a strong believer in continuous education:
- Online courses (Coursera, Udemy, AWS Training)
- Technical documentation and whitepapers
- Engineering blogs and case studies
- Conference talks and tech presentations
- Books on software design, architecture, and AI

**Practical Application**
His education combines academic theory with practical implementation through personal projects, open-source contributions, and professional work.

The software engineering field evolves rapidly, so he stays current through constant learning and experimentation!""",

        """Sushen's education includes:

**Academic Background**
- Bachelor's degree in Computer Science or related engineering field
- Strong theoretical foundation in CS fundamentals
- Graduated with knowledge of core concepts: algorithms, data structures, system design, databases

**Academic Focus Areas**
During his studies, he concentrated on:
- Software engineering principles
- Web and mobile application development
- Database management systems
- Cloud computing concepts
- AI and machine learning fundamentals

**Post-Graduation Learning**
The tech industry changes fast, so he continuously updates his skills:
- AWS and cloud platform certifications
- AI/ML courses and hands-on projects
- Framework-specific learning (React, FastAPI, etc.)
- System design and architecture studies
- DevOps and infrastructure best practices

**Learning Philosophy**
He treats education as an ongoing process, not a one-time achievement. Every project is an opportunity to learn something new, whether it's a programming language, cloud service, or architectural pattern.

This combination of formal education and continuous learning keeps his skills sharp and relevant!"""
    ],

    "how can i contact him?": [
        """You can reach Sushen through several channels:

**Email**
The most reliable way to contact him for professional inquiries, collaboration opportunities, or questions.

**LinkedIn**
Connect with him for professional networking and to see his career updates.

**GitHub**
Check out his code repositories and open-source contributions. You can also open issues or discussions on his projects.

**This Chatbot**
You can leave a message here and it will be logged for him to review!

**What to Reach Out About**
- Job opportunities or consulting work
- Collaboration on interesting projects
- Technical questions or advice
- Speaking at meetups or conferences
- Open-source contributions

He's generally responsive to genuine professional inquiries and is always interested in discussing technology and solving interesting problems!""",

        """Here are the best ways to get in touch with Sushen:

**Professional Inquiries**
- **Email**: Best for detailed discussions, job opportunities, or project proposals
- **LinkedIn**: Great for professional networking and staying connected

**Technical Discussions**
- **GitHub**: For code-related questions, issues, or contributions to his projects
- **Blog Comments**: Respond to his blog posts for topic-specific discussions

**General Contact**
You can also use this chatbot to leave a message! While I'm an AI, conversations are logged and he reviews them.

**Response Time**
He typically responds within 1-2 business days for professional emails. GitHub issues and LinkedIn messages may take slightly longer depending on volume.

**What He's Interested In**
- Innovative tech projects
- Consulting opportunities
- Speaking engagements
- Technical collaboration
- Open-source contributions

Feel free to reach out - he's approachable and enjoys connecting with fellow engineers and tech enthusiasts!""",

        """Sushen is available through multiple communication channels:

**Primary Contact Methods**
1. **Email**: Best for formal inquiries, job opportunities, or detailed discussions
2. **LinkedIn**: Professional networking and career-related connections
3. **GitHub**: Technical questions, code reviews, or collaboration on projects

**Social & Community**
He may also be active on:
- Twitter/X for tech discussions
- Dev.to or Medium for blog cross-posts
- Technical Slack/Discord communities
- Conference networking events

**Response Expectations**
- Email: 1-2 business days
- LinkedIn: 2-3 days
- GitHub: Varies based on project activity
- This chatbot: Messages are logged and reviewed

**Best Practices When Reaching Out**
- Be clear about your purpose (job, collaboration, question, etc.)
- Include relevant context
- For technical questions, provide details about your use case
- For opportunities, share specifics about the role or project

**Topics He Enjoys Discussing**
- Cloud architecture and AWS
- AI/ML applications
- System design challenges
- Interesting technical problems
- Industry trends and best practices

Don't hesitate to reach out - he values meaningful professional connections!"""
    ],

    "tell me a fun fact about sushen": [
        """Here's something interesting about Sushen:

He built this very chatbot you're talking to! It's a fully serverless AI assistant running on AWS that can answer questions about him by querying his portfolio data, blog posts, and professional background.

The chatbot features:
- Real-time streaming responses
- Conversation context management
- Knowledge retrieval from multiple sources
- Rate limiting and authentication
- Deployed entirely on AWS Lambda

Not only does it showcase his technical skills, but it also provides an interactive way for visitors to learn about him instead of just reading a static resume. Pretty meta, right?

He believes in "learning by building" - this chatbot was both a learning project for AWS Bedrock/AI agents and a practical tool for his portfolio!""",

        """Fun fact: Sushen is a strong advocate for "building in public" and learning by doing!

Instead of just reading documentation or taking courses, he learns new technologies by building real projects with them. This portfolio website itself is a testament to that approach - it's not just a static site, but a full-stack application with:
- AI chatbot (that's me!)
- Blog platform
- Analytics tracking
- Serverless backend
- CI/CD deployment

Each feature was an opportunity to learn something new: AWS Bedrock for AI, Lambda for serverless, DynamoDB for NoSQL databases, Next.js for modern React, etc.

He often says "the best way to learn a technology is to build something meaningful with it" - and you can see that philosophy reflected throughout his work.

His projects aren't just portfolio pieces; they're functional applications that solve real problems while demonstrating technical skills!""",

        """Here's an interesting tidbit:

Sushen has a particular interest in the intersection of AI and traditional software engineering. While many developers either focus on "classical" software development OR dive deep into ML/AI, he enjoys combining both:

- Building production-grade applications (proper architecture, testing, deployment)
- Enhanced with AI capabilities (LLMs, chatbots, intelligent features)
- Deployed on modern cloud infrastructure (serverless, scalable, cost-effective)

This "best of both worlds" approach means his AI applications aren't just proof-of-concepts - they're robust systems with proper error handling, monitoring, authentication, and all the things production software needs.

You're experiencing this right now! This chatbot isn't just a simple AI wrapper - it has:
- Rate limiting to prevent abuse
- API key authentication
- Streaming responses for better UX
- Conversation history management
- Graceful error handling
- Production deployment on AWS

He believes AI should enhance well-engineered software, not replace good engineering practices!""",

        """A cool fact about Sushen:

He's particularly passionate about developer experience (DX) and building tools that other developers would actually want to use. This extends to:

**Documentation**
He writes detailed technical documentation and blog posts explaining not just what he built, but WHY certain decisions were made and what tradeoffs were considered.

**Code Quality**
His code is written with the next developer in mind - clear variable names, logical structure, helpful comments where needed, and comprehensive error messages.

**API Design**
When building APIs, he thinks carefully about the developer experience: intuitive endpoints, consistent response formats, helpful error messages, and good documentation.

**Open Source**
He contributes to open-source projects and shares his own code, believing that good software should be accessible and understandable.

**Learning Resources**
His blog posts often include full code examples, configuration files, and step-by-step explanations so others can learn from his experience.

This focus on DX comes from his own experience as a developer - he builds the kind of tools and documentation he wishes existed when he was learning!"""
    ],

    "what technologies does he work with?": [
        """Sushen works with a modern, production-ready tech stack:

**Backend**
- **Python**: FastAPI, Flask, Django
- **Java**: Spring Boot for enterprise applications
- **Node.js**: Express, serverless functions

**Frontend**
- **React**: Functional components, hooks, context
- **Next.js**: SSR, SSG, API routes, App Router
- **TypeScript**: Type-safe development
- **Styling**: Tailwind CSS, styled-components

**Cloud & Infrastructure (AWS)**
- **Compute**: Lambda, ECS, EC2
- **Storage**: S3, DynamoDB, RDS (PostgreSQL)
- **AI**: Bedrock, SageMaker
- **Networking**: API Gateway, CloudFront, Route53
- **IaC**: CloudFormation, Serverless Framework

**AI & Data**
- **LLMs**: AWS Bedrock (Claude, etc.)
- **Vector DBs**: Pinecone, ChromaDB
- **Frameworks**: LangChain, custom RAG implementations

**DevOps**
- Git, GitHub Actions, Docker, CI/CD

**Databases**
- PostgreSQL, MongoDB, DynamoDB, Redis

This stack allows him to build full-stack, cloud-native, AI-powered applications end-to-end!""",

        """Here's Sushen's technology toolbox:

**Programming Languages**
- **Python** (primary backend language)
- **TypeScript/JavaScript** (frontend and Node.js)
- **Java** (enterprise applications)
- **SQL** (database queries)
- **Bash** (scripting and automation)

**Web Frameworks**
- FastAPI - Modern Python web framework
- React - Frontend library
- Next.js - React framework with SSR
- Spring Boot - Java enterprise framework
- Express - Node.js framework

**Cloud Platform: AWS**
- Lambda & Function URLs (serverless compute)
- API Gateway (API management)
- DynamoDB (NoSQL database)
- S3 (object storage)
- Bedrock (AI/ML services)
- CloudFormation (infrastructure as code)
- CloudWatch (monitoring)

**AI Technologies**
- AWS Bedrock (Claude, Titan models)
- LLM prompt engineering
- RAG (Retrieval Augmented Generation)
- Vector embeddings and similarity search

**Data & Databases**
- PostgreSQL (relational)
- MongoDB (document)
- DynamoDB (key-value)
- Redis (caching)

**Tools & Practices**
- Git for version control
- Docker for containerization
- CI/CD pipelines
- Testing frameworks (pytest, Jest)
- API design (REST, GraphQL)

Modern, scalable, and production-proven!""",

        """Sushen's technical toolkit spans the full stack:

**Core Stack**
- **Backend**: Python (FastAPI, Django), Java (Spring Boot)
- **Frontend**: React, Next.js, TypeScript
- **Database**: PostgreSQL, DynamoDB, MongoDB, Redis
- **Cloud**: AWS (Lambda, S3, API Gateway, Bedrock, etc.)

**AI & Machine Learning**
- AWS Bedrock for LLM integration
- Custom chatbot development
- RAG (Retrieval Augmented Generation) systems
- Prompt engineering and optimization
- Vector databases for semantic search

**Infrastructure & DevOps**
- Serverless architecture (AWS Lambda)
- Infrastructure as Code (CloudFormation, Terraform)
- Docker containers
- CI/CD with GitHub Actions
- Monitoring with CloudWatch

**Development Tools**
- VS Code as primary IDE
- Git for version control
- Postman for API testing
- AWS CLI for cloud management
- Various debugging and profiling tools

**Current Focus**
He's particularly deep into:
- AI integration in web applications
- Serverless architecture patterns
- Full-stack TypeScript development
- Cloud cost optimization
- Real-time features (WebSockets, streaming)

**Learning Next**
The tech world evolves fast! He's always exploring new tools and frameworks to stay current.

His approach: master the fundamentals, then learn specific tools as needed for each project!"""
    ]
}


def normalize_question(question: str) -> str:
    """Normalize a question for cache lookup."""
    return question.lower().strip().rstrip('?').strip()


def get_cached_response(user_message: str) -> Optional[str]:
    """
    Get a random cached response for a user message if available.

    Args:
        user_message: The user's message/question

    Returns:
        A random cached response if available, None otherwise
    """
    normalized = normalize_question(user_message)

    # Check if this matches any cached prompt
    if normalized in RESPONSE_CACHE:
        responses = RESPONSE_CACHE[normalized]
        # Randomly select one of the cached responses
        return random.choice(responses)

    return None


def get_all_cached_prompts() -> List[str]:
    """Get all prompts that have cached responses."""
    return list(RESPONSE_CACHE.keys())
