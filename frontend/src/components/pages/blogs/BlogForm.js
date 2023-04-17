import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import AlertPopup from '../../reusable/AlertPopup'
import wretch from 'wretch'

const CreateBlogPost = () => {
    const { id } = useParams()
    const [title, setTitle] = useState('')
    const [text, setText] = useState('')

    const [showAlert, setShowAlert] = useState(false)

    const setFormValues = (blog) => {
        setTitle(blog.title)
        setText(blog.text)
    }

    useEffect(() => {
        const fetchBlogData = async () => {
            wretch(`http://localhost:5000/api/v1/blogs/${id}`)
                .get()
                .json(data => setFormValues(data.blog))
                .catch(err => console.log(err))
        }
        if (id) {
            fetchBlogData()
        }
    }, [])

    const createBlogPost = async (title, text) => {
        let response = null
        const data = { title, text }
        if (id) {
            response = wretch(`http://localhost:5000/api/v1/blogs/${id}/`).put(data)
        } else {
            response = wretch('http://localhost:5000/api/v1/blogs').post(data)
        }

        response
            .res(response => console.log('response: ', response))
            .catch(err => console.log('error: ', err))
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        // Handle form submission logic here
        createBlogPost(title, text)
    }

    return (
        <div className="w-full max-w-md mx-auto mt-6">
            <form onSubmit={handleSubmit} className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="title">
                        Title
                    </label>
                    <input
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        id="title"
                        type="text"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                    />
                </div>
                <div className="mb-6">
                    <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="text">
                        Text
                    </label>
                    <textarea
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        id="text"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        rows="5"
                    ></textarea>
                </div>
                <div className="flex items-center justify-between">
                    <button
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                        type="submit"
                    >
                        { id ? 'Update Blog' : 'Add Blog' }
                    </button>
                </div>
            </form>

            { showAlert && <AlertPopup message="There was an error creating the post" type="error" onClose={() => setShowAlert(false)}/>}
        </div>
    )
}

export default CreateBlogPost
