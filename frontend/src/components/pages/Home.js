import profilePic from '../../images/Sutturu_Sushen_wsp.jpg'
import FeaturedProjects from './FeaturedProjects'

const Home = () => {
    return (
        <>
            <div className="bg-primary text-primary">
                <div className="container mx-auto px-4 py-10">
                    <div className='bg-white px-10 py-16'>
                        <div className="grid grid-cols-1 py-10 md:grid-cols-2 gap-8 flex items-center">
                            <div>
                                <h1 className="text-2xl md:text-4xl font-bold mb-6">
                                    Hey, I&apos;m
                                    <span className="text-highlight"> Sushen</span> - A Software Engineer from Melbourne.
                                </h1>
                                <p className="text-md md:text-xl">
                                    I have a passion for building robust, scalable and reliable software systems.
                                    Explore my latest projects, learn more about me and get in touch.
                                </p>
                                <p className="text-md md:text-xl">

                                </p>
                                <div className="flex mt-10">
                                    <a
                                        href="/portfolio"
                                        className="border-2 border-highlight text-primary py-2 px-4 rounded-md font-semibold hover:bg-opacity-40 transition duration-200"
                                    >
                                        Portfolio
                                    </a>
                                    <a
                                        href="/blog"
                                        className="border-2 border-secondary text-primary py-2 px-7 ml-4 rounded-md font-semibold hover:bg-highlight hover:text-white transition duration-200"
                                    >
                                        Blog
                                    </a>
                                </div>
                            </div>
                            <div className='justify-self-end'>
                                <img
                                    src={profilePic}
                                    alt="Photo"
                                    className="ml-auto w-3/4 object-cover"
                                />
                            </div>

                        </div>
                        <hr className='my-12' />
                        <FeaturedProjects />
                    </div>

                </div>
            </div>
        </>
    )
}

export default Home
