import Link from "next/link";

export default function About() {
    return (
        <section id="about" className="py-16 bg-gray-50 dark:bg-gray-800">
            <div className="container mx-auto px-4 md:px-6">
                <h2 className="text-3xl font-bold text-center mb-8 text-gray-900 dark:text-white">
                    About Me
                </h2>

                <div className="max-w-3xl mx-auto">

                    <p className="text-lg text-gray-700 dark:text-gray-300 mb-6">
                        Hey I'm Sushen,
                        A Software Engineer based in Melbourne, Australia.
                    </p>

                    <p className="text-lg text-gray-700 dark:text-gray-300 mb-6">
                        I'm currently working at TeamAssurance as a Full Stack Developer, creating software for global manufacturing customers.
                    </p>

                    <p className="text-lg text-gray-700 dark:text-gray-300 mb-6">
                        Working with React, Node, AWS and MySQL.
                        Working at a startup requires me to operate across the full stack, contributing to everything from designing intuitive user interfaces to configuring infrastructure within the AWS ecosystem.
                    </p>

                    <p className="text-lg text-gray-700 dark:text-gray-300 mb-6">
                        When I'm not coding, you can find me reading the latest non fiction or fantasy books, expanding my smart home setup,
                        or playing my favourite sports in badminton, pickleball or tennis.
                    </p>

                    <p className="text-lg text-gray-700 dark:text-gray-300">
                        You can check out some of the projects I've worked on in my spare time on the <Link href="/projects" className="text-blue-600 dark:text-blue-400 hover:underline font-medium">projects page</Link>.
                        I'd love to hear your thoughts!
                    </p>
                </div>
            </div>
        </section>
    );
} 