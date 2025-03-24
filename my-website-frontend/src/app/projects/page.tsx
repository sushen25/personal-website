import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import ProjectCard from "@/components/ProjectCard";

export default function Projects() {
    // Replace with your actual projects data
    const projects = [
        {
            title: "Project One",
            description: "A web application built with React and Node.js that allows users to track their daily habits and progress over time.",
            imageSrc: "/project1.jpg", // Add actual image later
            tags: ["React", "Node.js", "MongoDB", "Express"],
            projectUrl: "https://project1.example.com",
            githubUrl: "https://github.com/yourusername/project1"
        },
        {
            title: "Project Two",
            description: "An e-commerce platform with secure payment processing, product catalog, and user authentication.",
            imageSrc: "/project2.jpg", // Add actual image later
            tags: ["Next.js", "Stripe", "Firebase", "Tailwind CSS"],
            projectUrl: "https://project2.example.com",
            githubUrl: "https://github.com/yourusername/project2"
        },
        {
            title: "Project Three",
            description: "A mobile-responsive dashboard that visualizes data from multiple sources with real-time updates.",
            imageSrc: "/project3.jpg", // Add actual image later
            tags: ["TypeScript", "React", "D3.js", "GraphQL"],
            projectUrl: "https://project3.example.com",
            githubUrl: "https://github.com/yourusername/project3"
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
                                projectUrl={project.projectUrl}
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