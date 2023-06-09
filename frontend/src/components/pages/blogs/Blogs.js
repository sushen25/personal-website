import React, { useState, useEffect } from 'react'
import wretch from 'wretch'
import { useAuth } from '../../context/AuthContext'

const BlogList = () => {
    const [blogs, setBlogs] = useState([])
    const auth = useAuth()

    useEffect(() => {
        const fetchBlogData = async () => {
            wretch('http://localhost:5000/api/v1/blogs/')
                .get()
                .json(data => setBlogs(data.blogs))
        }
        fetchBlogData()
    }, [])

    const deleteBlog = async (id) => {
        wretch(`http://localhost:5000/api/v1/blogs/${id}`)
            .delete()
            .res(response => {
                setBlogs(blogs.filter((blog) => blog.id !== id))
            })
    }

    return (
        <div className="max-w-2xl mx-auto mt-6">
            { auth.authenticated ? 'Yes' : 'No'}
            <a href="/blog/add">
                <button

                    className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded shadow"
                >
                Add Blog
                </button>
            </a>

            {blogs.map((blog) => (
                <div key={blog.id} className="bg-white shadow-md p-6 my-4 rounded-md relative">
                    <a href={`/blog/${blog.id}/update/`}>
                        <button
                            className="bg-blue-500 hover:bg-blue-600 text-white font-semibold text-xs py-1 px-2 rounded absolute top-2 right-2 mr-16"
                        >
                        Update
                        </button>
                    </a>
                    <button
                        className="bg-red-500 hover:bg-red-600 text-white font-semibold text-xs py-1 px-2 rounded absolute top-2 right-2"
                        onClick={() => deleteBlog(blog.id)}
                    >
                        Delete
                    </button>
                    <h2 className="text-2xl font-bold mb-2">{blog.title}</h2>
                    <p className="text-gray-700">{blog.text}</p>
                    <div className="mt-4 text-gray-500">{blog.createdAt}</div>
                </div>

            ))}
        </div>
    )
}

export default BlogList
