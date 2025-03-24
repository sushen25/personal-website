export default function About() {
    return (
        <section id="about" className="py-16 bg-gray-50 dark:bg-gray-800">
            <div className="container mx-auto px-4 md:px-6">
                <h2 className="text-3xl font-bold text-center mb-8 text-gray-900 dark:text-white">
                    About Me
                </h2>

                <div className="max-w-3xl mx-auto">
                    <p className="text-lg text-gray-700 dark:text-gray-300 mb-6">
                        {/* Replace with your LinkedIn summary */}
                        I'm a passionate software engineer focused on building robust and scalable applications.
                        With expertise in both frontend and backend development, I enjoy creating elegant solutions
                        to complex problems.
                    </p>

                    <p className="text-lg text-gray-700 dark:text-gray-300 mb-6">
                        My technical journey has equipped me with a diverse skill set, including modern JavaScript frameworks,
                        cloud technologies, and database systems. I'm dedicated to writing clean, maintainable code and
                        continuously expanding my knowledge to stay at the forefront of technology.
                    </p>

                    <p className="text-lg text-gray-700 dark:text-gray-300">
                        When I'm not coding, you can find me exploring new technologies, contributing to open-source projects,
                        or sharing my knowledge through technical writing and mentoring junior developers.
                    </p>
                </div>
            </div>
        </section>
    );
} 