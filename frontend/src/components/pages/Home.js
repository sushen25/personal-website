import profilePic from '../../images/profPic.jpeg'

const Home = () => {
    return (
        <header className="bg-primary text-primary">
            <div className="container mx-auto px-6 py-6 md:py-20 lg:mx-20 xl:px-24">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 flex items-center">
                    <div>
                        <h1 className="text-2xl md:text-4xl font-bold mb-6">
                            Hey, I'm
                            <span className="text-highlight"> Sushen</span> - A Software Engineer from Melbourne.
                        </h1>
                        <p className="text-md md:text-xl">
                            Explore my latest projects, learn more about me, and get in touch.
                        </p>
                        <div className="flex my-10">
                            <a
                                href="/contact"
                                className="bg-highlight border-2 border-highlight text-primary py-2 px-4 rounded-md font-semibold hover:bg-opacity-40 transition duration-200"
                            >
                                Contact
                            </a>
                            <a
                                href="/blog"
                                className="bg-primary border-2 border-secondary text-primary py-2 px-7 ml-4 rounded-md font-semibold hover:bg-highlight hover:text-primary transition duration-200"
                            >
                                Blog
                            </a>
                        </div>
                    </div>
                    <div>
                        <img src={profilePic} alt="Profile pic"/>
                    </div>
                </div>
            </div>
        </header>

    )
}

export default Home
