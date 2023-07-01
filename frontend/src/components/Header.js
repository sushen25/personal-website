import React from 'react'

const Header = () => {
    return (
        <>
            <nav className="bg-black text-primary p-4 shadow">
                <div className="mx-auto px-4 sm:px-6 md:px-8 lg:px-10 xl:px-12 2xl:px-14 max-w-screen-xl">
                    <div className="flex items-center justify-between text-white">

                        <div className="font-bold text-xl">
                            <a href="/">Sushen Satturu</a>
                        </div>

                        <div className="flex space-x-4">
                            <a href="/portfolio" className="hover:text-blue-500">
                            Portfolio
                            </a>
                            <a href="/blog" className="hover:text-blue-500">
                            Blog
                            </a>
                        </div>
                    </div>
                </div>
            </nav>
        </>
    )
}

export default Header
