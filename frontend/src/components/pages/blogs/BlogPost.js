
import React, { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faEdit, faTrash } from '@fortawesome/free-solid-svg-icons'

import ActionConfirmationModal from '../../reusable/ActionConfirmationModal'

const convertIsoToFormattedDate = (isoTimestamp) => {
    const dateObj = new Date(isoTimestamp)
    const options = { year: 'numeric', month: 'short', day: 'numeric' }
    return dateObj.toLocaleDateString('en-US', options)
}

const limitTextWithEllipsis = (text, limit) => {
    if (text.length <= limit) {
        return text
    } else {
        const truncatedText = text.slice(0, limit - 3) // Reserve space for "..."
        const lastSpaceIndex = truncatedText.lastIndexOf(' ')
        return truncatedText.slice(0, lastSpaceIndex) + '...'
    }
}

const BlogPost = ({ blog, auth, deleteBlog }) => {
    const [showDeleteModal, setShowDeleteModal] = useState(false)

    const openDeleteModal = (blog) => {
        setShowDeleteModal(true)
    }

    const closeDeleteModal = () => {
        setShowDeleteModal(false)
    }

    const confirmDelete = (blogId) => {
        deleteBlog(blogId)
        setShowDeleteModal(false)
    }

    return (
        <div key={blog.id}>
            <div className="text-gray-500">{convertIsoToFormattedDate(blog.createdAt)}</div>

            <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold mb-2">{blog.title}</h2>

                <div className="flex space-x-4">
                    {
                        auth.authenticated
                            ? (
                                <div className='space-x-3'>
                                    <a href={`/blog/${blog.id}/update/`}>
                                        <FontAwesomeIcon icon={faEdit} size="lg"/>
                                    </a>
                                    <FontAwesomeIcon icon={faTrash} size="lg" onClick={() => openDeleteModal(blog)}/>
                                </div>
                            )
                            : null
                    }

                </div>
            </div>

            <p className="text-gray-700">{limitTextWithEllipsis(blog.text, 500)}</p>

            <ActionConfirmationModal
                confirmationTitle='Confirm Delete'
                confirmationText={'Are you sure you want to delete this blog?'}
                isOpen={showDeleteModal}
                onClose={() => closeDeleteModal(false)}
                onConfirm={() => confirmDelete(blog.id)}
            />
        </div>
    )
}

export default BlogPost
