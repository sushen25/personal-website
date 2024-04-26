import React, { useState, useEffect } from 'react'
import { getAllBlogs } from '../../api/blogApi'
import { useAuth } from '../../context/AuthContext'

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

const BlogList = () => {
    const [blogs, setBlogs] = useState([])
    const auth = useAuth()

    useEffect(() => {
        getAllBlogs()
            .json((json) => {
                console.log(json)
            })
    }, [])

    const deleteBlog = async (id) => {
        wretch(`http://localhost:5000/api/v1/blogs/${id}`)
            .delete()
            .res(response => {
                setBlogs(blogs.filter((blog) => blog.id !== id))
            })
    }

    return (
        <div className="bg-primary text-primary">
            <div className="container mx-auto px-4 py-10">
                <div className='bg-white px-10 py-16 text-primary'>
                    <h1 className='text-primary text-4xl'>Blog</h1>
                    {
                        auth.authenticated
                            ? (
                                <a href="/blog/add">
                                    <button

                                        className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded shadow"
                                    >
                                        Add Blog
                                    </button>
                                </a>
                            )
                            : null
                    }

                    <div className='my-8'/>

                    {blogs.map((blog, index) => {
                        return (
                            <div key={blog.id}>
                                <div className="text-gray-500">{convertIsoToFormattedDate(blog.createdAt)}</div>
                                <h2 className="text-2xl font-bold mb-2">{blog.title}</h2>
                                { auth.authenticated
                                    ? (
                                        <div>
                                            <a href={`/blog/${blog.id}/update/`}>
                                                <button
                                                    className="bg-blue-500 hover:bg-blue-600 text-white font-semibold text-xs py-1 px-2 rounded mr-2"
                                                >
                                        Update
                                                </button>
                                            </a>
                                            <button
                                                className="bg-red-500 hover:bg-red-600 text-white font-semibold text-xs py-1 px-2 rounded"
                                                onClick={() => deleteBlog(blog.id)}
                                            >
                                    Delete
                                            </button>
                                        </div>
                                    )
                                    : null}

                                <p className="text-gray-700">{limitTextWithEllipsis(blog.text, 500)}</p>

                                {index < blogs.length - 1 ? (<hr className='my-8'/>) : null}
                            </div>
                        )
                    })}
                </div>
            </div>
        </div>
    )

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
                    { auth.authenticated
                        ? (
                            <div>
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
                            </div>
                        )
                        : null}

                    <h2 className="text-2xl font-bold mb-2">{blog.title}</h2>
                    <p className="text-gray-700">{blog.text}</p>
                    <div className="mt-4 text-gray-500">{blog.createdAt}</div>
                </div>

            ))}
        </div>
    )
}

export default BlogList
