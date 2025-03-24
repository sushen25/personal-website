import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";

export default function Resume() {
    return (
        <div className="min-h-screen">
            <Navbar />

            <main className="pt-24 pb-16">
                <div className="container mx-auto px-4 md:px-6">
                    <div className="max-w-3xl mx-auto bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg">
                        <h1 className="text-4xl font-bold mb-8 text-center text-gray-900 dark:text-white">
                            Resume
                        </h1>

                        <div className="flex justify-center mb-10">
                            <Link
                                href="/resume.pdf"
                                target="_blank"
                                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                                    <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
                                </svg>
                                Download Resume PDF
                            </Link>
                        </div>

                        <div className="mb-8">
                            <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Resume Overview</h2>
                            <p className="text-gray-700 dark:text-gray-300">
                                This is a placeholder for your resume content. You can either embed your PDF resume here
                                or provide a direct download link (as shown above). Additionally, you might want to include
                                a brief overview of your resume or your professional summary.
                            </p>
                        </div>

                        <div className="mb-8">
                            <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">What's Included</h2>
                            <ul className="list-disc pl-5 space-y-2 text-gray-700 dark:text-gray-300">
                                <li>Professional Experience</li>
                                <li>Technical Skills</li>
                                <li>Education</li>
                                <li>Projects</li>
                                <li>Certifications</li>
                                <li>Contact Information</li>
                            </ul>
                        </div>

                        <div>
                            <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Note</h2>
                            <p className="text-gray-700 dark:text-gray-300">
                                For a more detailed view of my experience and skills, please download the complete
                                resume PDF or explore the other sections of this website.
                            </p>
                        </div>
                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
} 