import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import ProjectCard from "@/components/ProjectCard";

export default function Projects() {
    // Replace with your actual projects data
    const projects = [
        {
            title: "My Checklist Generator",
            description: "A checklist generator that allows you to create any checklists in a pinch, using AI Agents.",
            imageSrc: "/checklist-generator-generator-example.png",
            tags: ["AI Agents", "CrewAI", "Streamlit", "Python", "OpenAI", "LangChain"],
            githubUrl: "https://github.com/sushen25/my-checklist-generator-ai"
        },
        {
            title: "Hacker News Chat",
            description: "An LLM RAG application that allows you to chat with Hacker News articles.",
            imageSrc: "/hacker-news-chat-photo.png",
            tags: ["AI", "LLM", "RAG", "Python", "Flask", "LangChain", "OpenAI", "Serverless"],
            githubUrl: "https://github.com/sushen25/hacker-news-chat-ai"
        },
        {
            title: "Calo Trak",
            description: "An iOS app that allows you to track your calories and macros, with external food API integration.",
            imageSrc: "/calo-trak-photo.png",
            tags: ["Swift", "SwiftUI", "XCode", "CoreData", "Firebase", "Mobile Development"],
            githubUrl: "https://github.com/sushen25/calorie-tracker"
        },
        // Add more projects as needed
    ];

    return (
        <div className="min-h-screen">
            <Navbar />

            <main className="pt-24 pb-16">
                <div className="container mx-auto px-4 md:px-6">
                    <h1 className="text-4xl font-bold text-center mb-12 text-gray-900 dark:text-white">
                        My Projects
                    </h1>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {projects.map((project, index) => (
                            <ProjectCard
                                key={index}
                                title={project.title}
                                description={project.description}
                                imageSrc={project.imageSrc}
                                tags={project.tags}
                                githubUrl={project.githubUrl}
                            />
                        ))}
                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
} 