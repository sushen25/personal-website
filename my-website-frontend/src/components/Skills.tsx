export default function Skills() {
    // Replace with your actual skills from LinkedIn
    const skills = [
        "JavaScript", "TypeScript", "React", "Next.js",
        "Node.js", "Express", "Python", "SQL",
        "MongoDB", "AWS", "Docker", "Git",
        "CSS", "Tailwind CSS", "RESTful APIs", "GraphQL"
    ];

    return (
        <section className="py-16 bg-gray-50 dark:bg-gray-800">
            <div className="container mx-auto px-4 md:px-6">
                <h2 className="text-3xl font-bold text-center mb-8 text-gray-900 dark:text-white">
                    Skills
                </h2>

                <div className="max-w-4xl mx-auto">
                    <div className="flex flex-wrap justify-center gap-3">
                        {skills.map((skill, index) => (
                            <span
                                key={index}
                                className="px-4 py-2 bg-white dark:bg-gray-700 rounded-full text-gray-700 dark:text-gray-200 shadow-sm border border-gray-200 dark:border-gray-600"
                            >
                                {skill}
                            </span>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
} 