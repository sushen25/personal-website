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
                                    Explore my latest projects, learn more about me, and get in touch.
                                </p>
                                <div className="flex mt-10">
                                    <a
                                        href="/contact"
                                        className="-border-2 border-highlight text-primary py-2 px-4 rounded-md font-semibold hover:bg-opacity-40 transition duration-200"
                                    >
                                        Contact
                                    </a>
                                    <a
                                        href="/blog"
                                        className="border-2 border-secondary text-primary py-2 px-7 ml-4 rounded-md font-semibold hover:bg-primary hover:text-primary transition duration-200"
                                    >
                                        Blog
                                    </a>
                                </div>
                            </div>
                            <div>
                                <img
                                    src={profilePic}
                                    alt="Photo"
                                    className="mx-auto w-1/2 object-cover"
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
