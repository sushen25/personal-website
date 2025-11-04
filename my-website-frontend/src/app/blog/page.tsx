import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";
import { posts } from "./posts";

export default function Blog() {
    // Sort posts by date (newest first)
    const sortedPosts = [...posts].sort((a, b) => {
        return new Date(b.date).getTime() - new Date(a.date).getTime();
    });

    return (
        <div className="min-h-screen">
            <Navbar />

            <main className="pt-24 pb-16">
                <div className="container mx-auto px-4 md:px-6">
                    <h1 className="text-4xl font-bold text-center mb-12 text-gray-900 dark:text-white">
                        My Blog
                    </h1>

                    <div className="max-w-4xl mx-auto">
                        <div className="space-y-6">
                            {sortedPosts.map((post, index) => (
                                <Link
                                    key={index}
                                    href={`/blog/${post.slug}`}
                                    className="block p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 border border-gray-200 dark:border-gray-700"
                                >
                                    <div className="flex flex-col md:flex-row md:items-stretch gap-6">
                                        <div className="flex-1">
                                            <h2 className="text-2xl font-semibold mb-2 text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400">
                                                {post.title}
                                            </h2>
                                            <p className="text-sm text-gray-500 dark:text-gray-400 mb-3">
                                                {new Date(post.date).toLocaleDateString('en-US', {
                                                    year: 'numeric',
                                                    month: 'long',
                                                    day: 'numeric'
                                                })}
                                            </p>
                                            {post.tags && post.tags.length > 0 && (
                                                <div className="flex flex-wrap gap-2 mt-4">
                                                    {post.tags.map((tag, tagIndex) => (
                                                        <span
                                                            key={tagIndex}
                                                            className="px-3 py-1 text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full"
                                                        >
                                                            {tag}
                                                        </span>
                                                    ))}
                                                </div>
                                            )}
                                        </div>
                                        {post.thumbnail && (
                                            <div className="flex-shrink-0 w-full md:w-64 h-full relative rounded-lg overflow-hidden">
                                                <img
                                                    src={post.thumbnail}
                                                    alt={post.title}
                                                    className="w-full h-full object-cover rounded-lg"
                                                />
                                            </div>
                                        )}
                                    </div>
                                </Link>
                            ))}
                        </div>

                        {sortedPosts.length === 0 && (
                            <div className="text-center py-12 text-gray-500 dark:text-gray-400">
                                <p>No blog posts yet. Check back soon!</p>
                            </div>
                        )}
                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
}

