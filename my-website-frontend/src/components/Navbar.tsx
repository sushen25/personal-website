"use client";

import Link from 'next/link';
import { useState } from 'react';

export default function Navbar() {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    return (
        <nav className="fixed top-0 left-0 w-full bg-white dark:bg-gray-900 shadow-md z-50 py-4">
            <div className="container mx-auto flex justify-between items-center px-4 md:px-6">
                <Link href="/" className="text-xl font-bold text-gray-800 dark:text-white">
                    Sushen Satturu
                </Link>

                {/* Mobile menu button */}
                <div className="md:hidden">
                    <button
                        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                        className="focus:outline-none"
                        aria-label="Toggle mobile menu"
                    >
                        <svg className="w-6 h-6 text-gray-800 dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path>
                        </svg>
                    </button>
                </div>

                {/* Desktop menu */}
                <ul className="hidden md:flex space-x-8">
                    <li>
                        <Link href="/#about" className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
                            About
                        </Link>
                    </li>
                    <li>
                        <Link href="/#experience" className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
                            Experience
                        </Link>
                    </li>
                    <li>
                        <Link href="/projects" className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
                            Projects
                        </Link>
                    </li>
                    <li>
                        <Link href="/resume" className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
                            Resume
                        </Link>
                    </li>
                    <li>
                        <Link href="/blog" className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
                            Blog
                        </Link>
                    </li>
                </ul>

                {/* Mobile menu overlay */}
                {isMobileMenuOpen && (
                    <div className="md:hidden fixed inset-0 bg-white dark:bg-gray-900 z-50 pt-20">
                        <div className="container mx-auto px-4">
                            <ul className="flex flex-col space-y-6">
                                <li>
                                    <Link
                                        href="/#about"
                                        className="block text-xl text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
                                        onClick={() => setIsMobileMenuOpen(false)}
                                    >
                                        About
                                    </Link>
                                </li>
                                <li>
                                    <Link
                                        href="/#experience"
                                        className="block text-xl text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
                                        onClick={() => setIsMobileMenuOpen(false)}
                                    >
                                        Experience
                                    </Link>
                                </li>
                                <li>
                                    <Link
                                        href="/projects"
                                        className="block text-xl text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
                                        onClick={() => setIsMobileMenuOpen(false)}
                                    >
                                        Projects
                                    </Link>
                                </li>
                                <li>
                                    <Link
                                        href="/resume"
                                        className="block text-xl text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
                                        onClick={() => setIsMobileMenuOpen(false)}
                                    >
                                        Resume
                                    </Link>
                                </li>
                                <li>
                                    <Link
                                        href="/blog"
                                        className="block text-xl text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
                                        onClick={() => setIsMobileMenuOpen(false)}
                                    >
                                        Blog
                                    </Link>
                                </li>
                            </ul>
                        </div>
                    </div>
                )}
            </div>
        </nav>
    );
} 