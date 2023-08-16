
import { useState } from 'react'

import education from '../../images/education.jpg'
import experience from '../../images/experience.jpg'

import awsLogo from '../../images/logos/aws logo.png'
import djangoLogo from '../../images/logos/django logo.png'
import dockerLogo from '../../images/logos/docker logo.webp'
import firebaseLogo from '../../images/logos/firebase logo.png'
import mongoLogo from '../../images/logos/mongo logo.png'
import nodeLogo from '../../images/logos/node logo.png'
import postgresLogo from '../../images/logos/postgres logo.png'
import reactLogo from '../../images/logos/react-logo.png'
import vueLogo from '../../images/logos/vue logo.png'

const containerWidth = 800 // Set the desired width of the container here
const imageSize = 150 // Set the desired width and height for each image
const spacing = 40 // Set the desired spacing between images

const TiledImageGallery = () => {
    const imageUrls = [reactLogo, vueLogo, djangoLogo, nodeLogo, postgresLogo, mongoLogo, awsLogo, firebaseLogo, dockerLogo]

    const numImages = imageUrls.length
    const totalImageWidth = imageSize + spacing
    const availableWidth = containerWidth - totalImageWidth
    const totalSpacing = (numImages - 1) * spacing
    const adjustedSpacing = availableWidth / numImages

    return (
        <div className="flex flex-wrap justify-center">
            {imageUrls.map((imageUrl, index) => {
                const marginLeft = index === 0 ? 0 : adjustedSpacing
                return (
                    <div key={index} className="my-4 rounded overflow-hidden" style={{ width: `${imageSize}px`, marginLeft }}>
                        <div className="aspect-w-4 aspect-h-3">
                            <img src={imageUrl} alt={`Image ${index + 1}`} className="object-cover object-center w-full h-full" />
                        </div>
                    </div>
                )
            })}
        </div>
    )
}

const Portfolio = () => {
    const [showAllEducationItems, setShowAllEducationItems] = useState(false)
    let educationItems = [
        { id: 1, dateRange: '2018-2022', title: 'Bachelor of Information Technology', subTitle: 'Monash University' },
        { id: 2, dateRange: '2018-2022', title: 'Bachelor of Commerce', subTitle: 'Monash University' },
        { id: 3, dateRange: '2016-2017', title: 'Victorian Certificate of Education', subTitle: 'John Monash Science School' }
    ]
    if (!showAllEducationItems) {
        educationItems = educationItems.splice(0, 2)
    }

    const [showAllExperienceItems, setShowAllExperienceItems] = useState(false)
    let experienceItems = [
        { id: 1, dateRange: 'Jan 2021 - Present', title: 'Software Engineer', subTitle: 'WSP' },
        { id: 2, dateRange: '', title: 'Junior Software Engineer', subTitle: 'WSP (Jul 2021 - Jun 2023)' },
        { id: 3, dateRange: '', title: 'Software Engineering Intern', subTitle: 'WSP (Jan 2021 - Jun 2021)' },
        { id: 4, dateRange: 'Oct 2017 - Dec 2021', title: 'Private Mathematics Tutor', subTitle: 'AIMS High Academy' }
    ]
    if (!showAllExperienceItems) {
        experienceItems = experienceItems.splice(0, 2)
    }

    return (
        <>
            <div className="bg-primary text-primary">
                <div className="container mx-auto px-4 py-10">
                    <div className='bg-white px-10 py-16'>
                        <h1 className="text-2xl md:text-4xl font-bold mb-6">Portfolio</h1>

                        <h3 className="text-xl md:text-md underline mb-5">Education and Experience</h3>
                        {/* TODO - animate expansion */}
                        {/* Education */}
                        <div className="grid lg:grid-cols-5 md:grid-cols-5 sm:grid-cols-1  gap-4">
                            <div className="col-span-2">
                                <img
                                    src={education}
                                    alt="Education Image"
                                />
                            </div>
                            <div className="col-span-3 bg-gray-300">
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
                                    <button className="bg-highlight ml-3 text-white font-bold py-1 px-2 rounded" onClick={() => setShowAllEducationItems(!showAllEducationItems)}>
                                        {showAllEducationItems ? 'See Less' : 'See More' }
                                    </button>
                                </div>
                            </div>
                        </div>

                        <hr className='my-10'/>

                        {/* Experience */}
                        <div className="grid grid-cols-5 gap-4">

                            <div className="col-span-3 bg-gray-300">
                                <div className="container py-2">
                                    <h3 className="text-xl md:text-md font-bold mb-5">Experience</h3>
                                    <table className='text-lg border-collapse w-full'>
                                        <tbody>
                                            {experienceItems.map((education) => (
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
                                    <button className="bg-highlight ml-3 text-white font-bold py-1 px-2 rounded" onClick={() => setShowAllExperienceItems(!showAllExperienceItems)}>
                                        {showAllExperienceItems ? 'See Less' : 'See More' }
                                    </button>
                                </div>
                            </div>
                            <div className="col-span-2">
                                <img
                                    src={experience}
                                    alt="Experience Image"
                                />
                            </div>
                        </div>

                        <hr className='my-10'/>

                        {/* Technical Skills */}
                        <h3 className="text-xl md:text-md underline mb-5">Technical Skills</h3>
                        <p className="text-primary">Throughout my career I've used the following technologies in a professional capacity on various non trivial applications.</p>

                        <div className="grid grid-cols-3 gap-4 my-4 text-primary text-lg">
                            <div className="col-span-1">
                                <strong>Frontend Frameworks</strong>
                                <ul className='ml-4 list-disc'>
                                    <li>React JS</li>
                                    <li>Vue JS</li>
                                </ul>

                                <div className='my-4'/>

                                <strong>Backend Frameworks</strong>
                                <ul className='ml-4 list-disc'>
                                    <li>Django</li>
                                    <li>Node JS</li>
                                </ul>

                                <div className='my-4'/>

                                <strong>Databases</strong>
                                <ul className='ml-4 list-disc'>
                                    <li>SQL Databases (Postgres, MySQL, etc.)</li>
                                    <li>Mongo DB</li>
                                    <li>Neo4J</li>
                                </ul>

                                <div className='my-4'/>

                                <strong>Cloud Infrastructure</strong>
                                <ul className='ml-4 list-disc'>
                                    <li>AWS</li>
                                    <li>Google Firebase</li>
                                </ul>

                                <div className='my-4'/>

                                <strong>Other</strong>
                                <ul className='ml-4 list-disc'>
                                    <li>Docker</li>
                                    <li>iOS (XCode)</li>
                                </ul>

                                <div className='my-4'/>
                            </div>
                            <div className="col-span-2">
                                <TiledImageGallery />
                            </div>
                        </div>

                        {/* TODO - Key Strengths */}

                        <hr className='my-10'/>

                        {/* Referees */}
                        <h3 className="text-xl md:text-md underline mb-5">Referees</h3>

                        <div className="text-lg">
                            <p>Mr. Madira Ginnige</p>
                            <p>CEO</p>
                            <p>AIMS High Academy</p>
                            <p>Tel: 0432 972 667</p>
                            <p>Email: madiraginige1@yahoo.com</p>
                        </div>

                    </div>
                </div>
            </div>
        </>
    )
}

export default Portfolio
