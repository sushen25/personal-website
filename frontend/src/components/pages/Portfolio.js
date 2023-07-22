
import education from '../../images/education.jpg'
import experience from '../../images/experience.jpg'

const Portfolio = () => {
    const educationItems = [
        { id: 1, dateRange: '2017-2022', title: 'Bachelor of Information Technology', subTitle: 'Monash University' },
        { id: 2, dateRange: '2017-2022', title: 'Bachelor of Commerce', subTitle: 'Monash University' },
        { id: 3, dateRange: '2016-2017', title: 'Victorian Certificate of Education', subTitle: 'John Monash Science School' }
    ]

    const experienceItems = [
        { id: 1, dateRange: '2017-2022', title: 'Bachelor of Information Technology', subTitle: 'Monash University' },
        { id: 2, dateRange: '2017-2022', title: 'Bachelor of Commerce', subTitle: 'Monash University' },
        { id: 3, dateRange: '2016-2017', title: 'Victorian Certificate of Education', subTitle: 'John Monash Science School' }
    ]

    return (
        <>
            <div className="bg-primary text-primary">
                <div className="container mx-auto px-4 py-10">
                    <div className='bg-white px-10 py-16'>
                        <h1 className="text-2xl md:text-4xl font-bold mb-6">Portfolio</h1>

                        <h3 className="text-xl md:text-md underline mb-5">Education and Experience</h3>
                        {/* Education */}
                        <div className="grid grid-cols-3 gap-4">
                            <div className="col-span-1">
                                <img
                                    src={education}
                                    alt="Education Image"
                                />
                            </div>
                            <div className="col-span-2 bg-gray-300">
                                <div className="container py-2">
                                    <h3 className="text-xl md:text-md font-bold mb-5">Education</h3>
                                    <table className='text-lg border-collapse w-full'>
                                        <tbody>
                                            {educationItems.map((education) => (
                                                <tr key={education.id}>
                                                    <td className='p-4 font-bold align-top'>{education.dateRange}</td>
                                                    <td className='p-4 align-top'>
                                                        <p>{education.title}</p>
                                                        <p className="text-sm">{education.subTitle}</p>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                    <button className="bg-highlight-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
                                        See more
                                    </button>
                                </div>
                            </div>
                        </div>

                        <hr className='my-10'/>

                        {/* Experience */}
                        <div className="grid grid-cols-3 gap-4">

                            <div className="col-span-2 bg-gray-300">
                                <div className="container py-2">
                                    <h3 className="text-xl md:text-md font-bold mb-5">Experience</h3>
                                    <table className='text-lg border-collapse w-full'>
                                        <tbody>
                                            {educationItems.map((education) => (
                                                <tr key={education.id}>
                                                    <td className='p-4 font-bold align-top'>{education.dateRange}</td>
                                                    <td className='p-4 align-top'>
                                                        <p>{education.title}</p>
                                                        <p className="text-sm">{education.subTitle}</p>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            <div className="col-span-1">
                                <img
                                    src={experience}
                                    alt="Experience Image"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Portfolio
