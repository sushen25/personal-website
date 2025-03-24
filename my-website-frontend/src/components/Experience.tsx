export default function Experience() {
    // Replace with your actual work experience from LinkedIn
    const experiences = [
        {
            title: "Software Engineer",
            company: "Company Name",
            duration: "Jan 2023 - Present",
            description: "Led development of key features for a SaaS platform, improving performance by 30%. Collaborated with cross-functional teams to implement best practices and new technologies."
        },
        {
            title: "Junior Developer",
            company: "Previous Company",
            duration: "May 2021 - Dec 2022",
            description: "Contributed to frontend and backend development of web applications. Implemented responsive design principles and integrated RESTful APIs."
        },
        // Add more experiences as needed
    ];

    return (
        <section id="experience" className="py-16">
            <div className="container mx-auto px-4 md:px-6">
                <h2 className="text-3xl font-bold text-center mb-8 text-gray-900 dark:text-white">
                    Work Experience
                </h2>

                <div className="max-w-3xl mx-auto">
                    <div className="relative border-l-2 border-gray-300 dark:border-gray-700 pl-8 ml-4">
                        {experiences.map((exp, index) => (
                            <div key={index} className="mb-10 relative">
                                {/* Timeline dot */}
                                <div className="absolute w-4 h-4 bg-blue-600 rounded-full -left-[2.65rem] top-1.5 border-4 border-white dark:border-gray-900"></div>

                                {/* Experience content */}
                                <h3 className="text-xl font-bold text-gray-900 dark:text-white">{exp.title}</h3>
                                <p className="text-blue-600 dark:text-blue-400 font-medium">{exp.company}</p>
                                <p className="text-sm text-gray-500 dark:text-gray-400 mb-3">{exp.duration}</p>
                                <p className="text-gray-700 dark:text-gray-300">{exp.description}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
} 