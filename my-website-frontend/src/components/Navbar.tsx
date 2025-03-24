import Link from 'next/link';

export default function Navbar() {
    return (
        <nav className="fixed top-0 left-0 w-full bg-white dark:bg-gray-900 shadow-md z-50 py-4">
            <div className="container mx-auto flex justify-between items-center px-4 md:px-6">
                <Link href="/" className="text-xl font-bold text-gray-800 dark:text-white">
                    Sushen Satturu
                </Link>

                {/* Mobile menu button */}
                <div className="md:hidden">
                    <button className="focus:outline-none">
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
                </ul>
            </div>
        </nav>
    );
} 