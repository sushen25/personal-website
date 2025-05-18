import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

export default function Resume() {
    return (
        <div className="min-h-screen flex flex-col">
            <Navbar />

            <main className="flex-1 pt-24 pb-16 flex flex-col items-center">
                <div className="container mx-auto px-4 md:px-6 max-w-4xl w-full">
                    <h1 className="text-4xl font-bold mb-8 text-center text-gray-900 dark:text-white">
                        Resume
                    </h1>
                    <div className="w-full h-[80vh] rounded-xl shadow-lg overflow-hidden bg-white dark:bg-gray-800">
                        <iframe
                            src="/resume.pdf"
                            title="Resume PDF"
                            className="w-full h-full"
                            frameBorder="0"
                        />
                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
} 