import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import Link from "next/link";
import Image from "next/image";

// API URL from environment variable
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

interface BlogPost {
    slug: string;
    title: string;
    publishedDate?: string;
    published_date?: string;
    tags?: string[];
    thumbnail?: string;
}

async function getPosts() {
    try {
        const res = await fetch(`${API_URL}/api/blog`, {
            cache: 'force-cache'
        });

        if (!res.ok) {
            console.error('Failed to fetch posts:', res.status, res.statusText);
            return [];
        }

        const posts = await res.json();
        return posts;
    } catch (error) {
        console.error('Error fetching posts:', error);
        return [];
    }
}

export default async function Blog() {
    const posts = await getPosts();

    // Sort posts by date (newest first) - API already sorts but double-check
    const sortedPosts = [...posts].sort((a: BlogPost, b: BlogPost) => {
        const dateB = b.publishedDate || b.published_date || '';
        const dateA = a.publishedDate || a.published_date || '';
        return new Date(dateB).getTime() - new Date(dateA).getTime();
    });

    return (
        <div className="min-h-screen">
            <Navbar />

            <main className="pt-24 pb-16">
                <div className="container mx-auto px-4 md:px-6">
                    <h1 className="text-4xl font-bold text-center mb-12 text-white">
                        My Blog
                    </h1>

                    <div className="max-w-4xl mx-auto">
                        <div className="space-y-6">
                            {sortedPosts.map((post, index) => (
                                <Link
                                    key={index}
                                    href={`/blog/${post.slug}`}
                                    className="block p-6 bg-gray-800 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 border border-gray-700"
                                >
                                    <div className="flex flex-col md:flex-row md:items-stretch gap-6">
                                        <div className="flex-1">
                                            <h2 className="text-2xl font-semibold mb-2 text-white hover:text-blue-400">
                                                {post.title}
                                            </h2>
                                            <p className="text-sm text-gray-400 mb-3">
                                                {new Date(post.publishedDate || post.published_date).toLocaleDateString('en-US', {
                                                    year: 'numeric',
                                                    month: 'long',
                                                    day: 'numeric'
                                                })}
                                            </p>
                                            {post.tags && post.tags.length > 0 && (
                                                <div className="flex flex-wrap gap-2 mt-4">
                                                    {post.tags.map((tag: string, tagIndex: number) => (
                                                        <span
                                                            key={tagIndex}
                                                            className="px-3 py-1 text-xs bg-blue-900 text-blue-200 rounded-full"
                                                        >
                                                            {tag}
                                                        </span>
                                                    ))}
                                                </div>
                                            )}
                                        </div>
                                        {post.thumbnail && (
                                            <div className="flex-shrink-0 w-full md:w-64 h-48 md:h-auto relative rounded-lg overflow-hidden">
                                                <Image
                                                    src={post.thumbnail}
                                                    alt={post.title}
                                                    fill
                                                    className="object-cover rounded-lg"
                                                    sizes="(max-width: 768px) 100vw, 256px"
                                                />
                                            </div>
                                        )}
                                    </div>
                                </Link>
                            ))}
                        </div>

                        {sortedPosts.length === 0 && (
                            <div className="text-center py-12 text-gray-400">
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

