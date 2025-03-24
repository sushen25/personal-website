export default function Education() {
    // Replace with your actual education from LinkedIn
    const education = [
        {
            degree: "Bachelor's Degree",
            school: "University Name",
            years: "2017 - 2021",
            description: "Graduated with honors. Relevant coursework included Data Structures, Algorithms, Web Development, and Database Systems."
        },
        // Add more education entries as needed
    ];

    return (
        <section className="py-16">
            <div className="container mx-auto px-4 md:px-6">
                <h2 className="text-3xl font-bold text-center mb-8 text-gray-900 dark:text-white">
                    Education
                </h2>

                <div className="max-w-3xl mx-auto">
                    {education.map((edu, index) => (
                        <div key={index} className="mb-8 bg-white dark:bg-gray-700 p-6 rounded-lg shadow-md">
                            <h3 className="text-xl font-bold text-gray-900 dark:text-white">{edu.degree}</h3>
                            <p className="text-blue-600 dark:text-blue-400 font-medium">{edu.school}</p>
                            <p className="text-sm text-gray-500 dark:text-gray-400 mb-3">{edu.years}</p>
                            <p className="text-gray-700 dark:text-gray-300">{edu.description}</p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
} 