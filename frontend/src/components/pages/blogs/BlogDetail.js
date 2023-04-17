import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import wretch from 'wretch'

const BlogDetail = () => {
    const { id } = useParams()
    const [blog, setBlog] = useState([])

    useEffect(() => {
        const fetchBlogData = async () => {
            wretch(`http://localhost:5000/api/v1/blogs/${id}`)
                .get()
                .json(data => setBlog(data.blog))
                .catch(err => console.log(err))
        }
        fetchBlogData()
    }, [])

    return (
        <div className="bg-white shadow-md p-6 my-4 rounded-md">
            <h2 className="text-2xl font-bold mb-2">{blog.title}</h2>
            <p className="text-gray-700">{blog.text}</p>
            <div className="mt-4 text-gray-500">
                {new Date(blog.createdAt).toLocaleDateString('en-US', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric'
                })}
            </div>
        </div>
    )
}

export default BlogDetail
