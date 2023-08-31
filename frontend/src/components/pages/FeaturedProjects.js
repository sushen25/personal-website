import React, { useState } from 'react'

import cityScape from '../../images/icmp.jpg'
import rdms from '../../images/rdms2.jpeg'

import IcmpProjectContent from './projectContent/IcmpProject.jsx'
import DermsProjectContent from './projectContent/DermsProject.jsx'
import FeaturedProjectModal from './FeaturedProjectModal.js'

const FeaturedProjects = () => {
    const [selectedProject, setSelectedProject] = useState({})
    const [projectModalOpen, setProjectModalOpen] = useState(false)

    const projects = [
        { id: 1, title: 'ICMP', fullTitle: 'Intelligent Congestion Management System (ICMP)', image: cityScape, content: IcmpProjectContent },
        { id: 2, title: 'RDMS', fullTitle: 'Resource Data Managagement System (RDMS)', image: rdms, content: DermsProjectContent }
        // { id: 3, title: 'iOS CaloTrak', fullTitle: 'iOS Calorie Tracking App', image: rdms },
        // { id: 4, title: 'Arduino Basketball', fullTitle: 'Arduino Basketball', image: rdms }
    ]

    function openModal (project) {
        setSelectedProject(project)
        setProjectModalOpen(true)
    }

    function closeModal () {
        setSelectedProject({})
        setProjectModalOpen(false)
    }

    return (

        <div>
            <h2 className="text-3xl font-bold mb-12">Featured Work</h2>
            <div className="grid grid-cols-2 gap-4">
                {projects.map((project) => (
                    <div
                        key={project.id}
                        onClick={() => openModal(project)}

                    >
                        <div className="relative overflow-hidden cursor-pointer">
                            <img
                                src={project.image}
                                alt={project.title}
                                className="w-full h-full object-cover"
                            />
                            <div className="absolute inset-0 bg-black bg-opacity-50 opacity-0 transition-opacity duration-300 hover:opacity-100">
                                <div className="flex items-center justify-center h-full">
                                    <p className="text-white font-bold text-xl">{project.title}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            <FeaturedProjectModal isOpen={projectModalOpen} onRequestClose={closeModal}>
                {selectedProject.content}
            </FeaturedProjectModal>
        </div>

    )
}

export default FeaturedProjects
