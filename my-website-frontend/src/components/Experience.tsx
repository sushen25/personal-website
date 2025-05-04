export default function Experience() {
    // Replace with your actual work experience from LinkedIn
    const experiences = [
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
            ]
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
            ]
        },
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
                            <div
                                key={index}
                                className="mb-8 relative bg-white/80 dark:bg-gray-900/70 rounded-lg shadow-sm border border-gray-200 dark:border-gray-800 px-6 py-4 transition hover:shadow-md"
                            >
                                {/* Timeline dot */}
                                <div className="absolute w-3 h-3 bg-blue-600 rounded-full -left-[2.5rem] top-4 border-4 border-white dark:border-gray-900"></div>

                                {/* Experience content */}
                                <h3 className="text-lg font-semibold text-gray-900 dark:text-white leading-tight mb-1">{exp.title}</h3>
                                <p className="text-blue-600 dark:text-blue-400 font-medium text-[15px] mb-0.5">{exp.company}</p>
                                <p className="text-xs text-gray-500 dark:text-gray-400 mb-2">{exp.duration}</p>
                                <ul className="list-disc list-inside text-gray-700 dark:text-gray-300 space-y-1 text-[15px] pl-1">
                                    {exp.description.map((point, idx) => (
                                        <li key={idx}>{point}</li>
                                    ))}
                                </ul>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
} 