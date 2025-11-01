import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import BlogContent from "@/components/BlogContent";
import Link from "next/link";
import { posts } from "../posts";
import { readFileSync } from "fs";
import { join } from "path";
import { notFound } from "next/navigation";

interface BlogPostPageProps {
    params: Promise<{
        slug: string;
    }>;
}

export async function generateStaticParams() {
    return posts.map((post) => ({
        slug: post.slug,
    }));
}

export default async function BlogPostPage({ params }: BlogPostPageProps) {
    const { slug } = await params;
    const post = posts.find((p) => p.slug === slug);

    if (!post) {
        notFound();
    }

    // Read the HTML article file
    const articlesPath = join(process.cwd(), "src/app/blog/articles", post.article);
    let articleContent = "";

    try {
        const fileContent = readFileSync(articlesPath, "utf-8");
        // Extract just the body content from the HTML
        const bodyMatch = fileContent.match(/<section[^>]*data-field="body"[^>]*>([\s\S]*?)<\/section>/);
        if (bodyMatch) {
            articleContent = bodyMatch[1];
        } else {
            // Fallback: try to get content from article tag
            const articleMatch = fileContent.match(/<article[^>]*>([\s\S]*?)<\/article>/);
            if (articleMatch) {
                articleContent = articleMatch[1];
            }
        }
    } catch (error) {
        console.error("Error reading article file:", error);
        articleContent = "<p>Error loading article content.</p>";
    }

    return (
        <div className="min-h-screen">
            <Navbar />

            <main className="pt-24 pb-16">
                <div className="container mx-auto px-4 md:px-6">
                    <div className="max-w-4xl mx-auto">
                        {/* Back to blog link */}
                        <Link
                            href="/blog"
                            className="inline-flex items-center text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 mb-8 transition-colors"
                        >
                            <svg
                                className="w-5 h-5 mr-2"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M15 19l-7-7 7-7"
                                />
                            </svg>
                            Back to Blog
                        </Link>

                        {/* Post header */}
                        <header className="mb-8">
                            <h1 className="text-4xl md:text-5xl font-bold mb-4 text-gray-900 dark:text-white">
                                {post.title}
                            </h1>
                            <p className="text-gray-600 dark:text-gray-400 mb-4">
                                {new Date(post.date).toLocaleDateString('en-US', {
                                    year: 'numeric',
                                    month: 'long',
                                    day: 'numeric'
                                })}
                            </p>
                            {post.tags && post.tags.length > 0 && (
                                <div className="flex flex-wrap gap-2">
                                    {post.tags.map((tag, index) => (
                                        <span
                                            key={index}
                                            className="px-3 py-1 text-sm bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full"
                                        >
                                            {tag}
                                        </span>
                                    ))}
                                </div>
                            )}
                        </header>

                        {/* Article content */}
                        <BlogContent html={articleContent} />
                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
}

