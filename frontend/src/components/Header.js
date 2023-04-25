import React from 'react'

const Header = () => {
    return (
        <nav className="bg-primary text-primary p-4 shadow">
            <div className="mx-auto px-4 sm:px-6 md:px-8 lg:px-10 xl:px-12 2xl:px-14 max-w-screen-xl">
                <div className="flex items-center justify-between">

                    <div className="font-bold text-xl">
                        <a href="/">Sushen</a>
                    </div>
                    <div className="flex space-x-4">
                        <a href="/" className="hover:text-blue-500">
                            Home
                        </a>
                        <a href="/blog" className="hover:text-blue-500">
                            Blog
                        </a>
                    </div>

                </div>
            </div>
        </nav>
    )
}

export default Header
