import React, { useState, useEffect } from 'react'
import wretch from 'wretch'
import { useAuth } from '../../context/AuthContext'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faAdd } from '@fortawesome/free-solid-svg-icons'

import BlogPost from './BlogPost.js'

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

    const deleteBlog = async (blogId) => {
        wretch(`http://localhost:5000/api/v1/blogs/${blogId}`)
            .delete()
            .res(response => {
                setBlogs(blogs.filter((blog) => blog.id !== blogId))
            })
    }

    return (
        <div className="bg-primary text-primary">
            <div className="container mx-auto px-4 py-10">
                <div className='bg-white px-10 py-16 text-primary'>

                    <div className="flex items-center justify-between">
                        <h1 className='text-4xl'>Blog</h1>

                        <div className="flex space-x-4">
                            {
                                auth.authenticated
                                    ? (
                                        <a href="/blog/add">
                                            <FontAwesomeIcon icon={faAdd} size="lg"/>
                                        </a>
                                    )
                                    : null
                            }

                        </div>
                    </div>

                    <div className='my-8'/>

                    {
                        blogs.map((blog, index) => {
                            return (
                                <div key={blog.id}>
                                    <BlogPost blog={blog} auth={auth} deleteBlog={deleteBlog} />
                                    {index !== blogs.length - 1 && <hr className='my-8' />}
                                </div>
                            )
                        })
                    }
                </div>
            </div>

        </div>
    )
}

export default BlogList
