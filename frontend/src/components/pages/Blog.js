import React, { useState, useEffect } from 'react'
import wretch from 'wretch'

const BlogList = () => {
    const [blogs, setBlogs] = useState([])

    useEffect(() => {
        const fetchBlogData = async () => {
            wretch('http://localhost:5000/api/v1/blogs/')
                .get()
                .json(data => setBlogs(data.blogs))
        }
        fetchBlogData()
    }, [])

    return (
        <div className="max-w-2xl mx-auto mt-6">
            <a href="/blog/add">
                <button

                    className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded shadow"
                >
                Add Blog
                </button>
            </a>

            {blogs.map((blog) => (
                <div key={blog.id} className="bg-white shadow-md p-6 my-4 rounded-md">
                    <h2 className="text-2xl font-bold mb-2">{blog.title}</h2>
                    <p className="text-gray-700">{blog.text}</p>
                    <div className="mt-4 text-gray-500">{blog.createdAt}</div>
                </div>
            ))}
        </div>
    )
}

export default BlogList
