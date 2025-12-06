// This file contains all the context about the user for the chatbot

export const getUserContext = () => {
    const about = {
        name: "Sushen Satturu",
        location: "Melbourne, Australia",
        currentRole: "Full Stack Developer at TeamAssurance",
        description: "A Software Engineer based in Melbourne, Australia. Currently working at TeamAssurance as a Full Stack Developer, creating software for global manufacturing customers using React, Node, AWS and MySQL. Working at a startup requires operating across the full stack, contributing to everything from designing intuitive user interfaces to configuring infrastructure within the AWS ecosystem.",
        hobbies: "Reading the latest non fiction or fantasy books, expanding smart home setup, playing badminton, pickleball or tennis"
    };

    const experience = [
        {
            title: "Full Stack Engineer",
            company: "TeamAssurance",
            duration: "Mar 2024 - Present",
            description: [
                "Develop and maintain full-stack applications in a fast-paced startup environment",
                "Design and implement cloud infrastructure solutions using AWS",
                "Collaborate with global clients including CSL, Suntory, and Pact",
                "Lead cross-functional development across UI, backend, and DevOps domains",
                "Build application integrations with third party APIs and Webhooks"
            ],
            skills: ["React", "TypeScript", "AWS", "Node.js", "Application Integrations", "Webhooks"]
        },
        {
            title: "Software Engineer",
            company: "WSP",
            duration: "Jan 2021 - Feb 2024",
            description: [
                "Delivered end-to-end software solutions for major clients including Australian Defence Force and Transport New South Wales",
                "Led technical mentorship program for interns and junior developers",
                "Ensured high-quality project delivery within strict timelines and requirements",
                "Implemented agile development methodologies to optimize team productivity"
            ],
            skills: ["Django", "Python", "VueJS", "Full Stack Development", "Mentorship"]
        }
    ];

    const education = [
        {
            degree: "Bachelor's of Computer Science",
            school: "Monash University",
            years: "2018 - 2021",
            description: "Graduated with honors. Relevant coursework included Data Structures, Algorithms, Web Development, and Database Systems."
        },
        {
            degree: "Bachelor's of Commerce",
            school: "Monash University",
            years: "2018 - 2021",
            description: "Relevant coursework included Finance, Economics, Business Law and Marketing."
        }
    ];

    const skills = [
        "JavaScript", "TypeScript", "React", "Next.js",
        "Node.js", "Express", "Python", "SQL",
        "MongoDB", "AWS", "Docker", "Git",
        "CSS", "Tailwind CSS", "RESTful APIs", "GraphQL",
        "AI Agents", "CrewAI", "Streamlit", "OpenAI",
        "Django", "VueJS"
    ];

    const projects = [
        {
            title: "My Checklist Generator",
            description: "A checklist generator that allows you to create any checklists in a pinch, using AI Agents.",
            tags: ["AI Agents", "CrewAI", "Streamlit", "Python", "OpenAI", "LangChain"],
            githubUrl: "https://github.com/sushen25/my-checklist-generator-ai"
        },
        {
            title: "Hacker News Chat",
            description: "An LLM RAG application that allows you to chat with Hacker News articles.",
            tags: ["AI", "LLM", "RAG", "Python", "Flask", "LangChain", "OpenAI", "Serverless"],
            githubUrl: "https://github.com/sushen25/hacker-news-chat-ai"
        },
        {
            title: "Calo Trak",
            description: "An iOS app that allows you to track your calories and macros, with external food API integration.",
            tags: ["Swift", "SwiftUI", "XCode", "CoreData", "Firebase", "iOS"],
            githubUrl: "https://github.com/sushen25/calorie-tracker"
        }
    ];

    const blogPosts = [
        {
            title: "Standardising AI Access - Model Context Protocol (MCP)",
            slug: "standardising-ai-access-model-context-protocol-mcp",
            date: "2025-10-09",
            tags: ["AI", "MCP", "Model Context Protocol", "Standardising AI Access"]
        }
    ];

    return {
        about,
        experience,
        education,
        skills,
        projects,
        blogPosts
    };
};

export const formatUserContextForPrompt = () => {
    const context = getUserContext();
    
    return `You are an AI assistant that helps answer questions about Sushen Satturu, a Software Engineer based in Melbourne, Australia. 

IMPORTANT: You should ONLY answer questions about Sushen's professional background, experience, skills, education, projects, and blog posts. You should NOT act as a general-purpose AI assistant. If asked about topics unrelated to Sushen, politely decline and redirect the conversation back to questions about Sushen.

Here is the information about Sushen:

ABOUT:
- Name: ${context.about.name}
- Location: ${context.about.location}
- Current Role: ${context.about.currentRole}
- Description: ${context.about.description}
- Hobbies: ${context.about.hobbies}

WORK EXPERIENCE:
${context.experience.map(exp => `
- ${exp.title} at ${exp.company} (${exp.duration})
  Description: ${exp.description.join('; ')}
  Skills: ${exp.skills.join(', ')}
`).join('\n')}

EDUCATION:
${context.education.map(edu => `
- ${edu.degree} from ${edu.school} (${edu.years})
  ${edu.description}
`).join('\n')}

SKILLS:
${context.skills.join(', ')}

PROJECTS:
${context.projects.map(proj => `
- ${proj.title}: ${proj.description}
  Technologies: ${proj.tags.join(', ')}
  GitHub: ${proj.githubUrl}
`).join('\n')}

BLOG POSTS:
${context.blogPosts.map(post => `
- ${post.title} (${post.date})
  Tags: ${post.tags.join(', ')}
`).join('\n')}

Remember: Only answer questions about Sushen. If asked about general topics, weather, current events, or anything unrelated to Sushen, politely say: "I'm designed to answer questions about Sushen Satturu's professional background. Is there something specific you'd like to know about his experience, skills, projects, or education?"`;
};

