// src/LoginForm.js
import React, { useState } from 'react'
import wretch from 'wretch'
import { useAuth } from '../context/AuthContext'

const Authentication = () => {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [message, setMessage] = useState('')
    const auth = useAuth()

    const handleSubmit = (e) => {
        e.preventDefault()

        wretch('http://localhost:5000/api/v1/login/')
            .post({ username, password })
            .json()
            .then((response) => {
                if (response.authenticated) {
                    setMessage('Authenticated successfully!')
                    auth.login(response.username)
                } else {
                    setMessage('Authentication failed')
                }
            })
            .catch((error) => {
                console.error(error)
                setMessage('An error occurred during authentication')
            })
    }

    return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center">
            <div className="bg-white p-8 rounded shadow-md w-full sm:w-96">
                <h1 className="text-2xl font-semibold mb-6">Login</h1>
                <form onSubmit={handleSubmit}>
                    <div className="mb-4">
                        <label className="block text-sm mb-2" htmlFor="username">
              Username
                        </label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-indigo-500"
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block text-sm mb-2" htmlFor="password">
              Password
                        </label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-indigo-500"
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full py-2 px-4 bg-indigo-600 text-white font-semibold rounded hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-opacity-75"
                    >
              Log In
                    </button>
                </form>
                {message && (
                    <p className="mt-4 text-sm text-center text-red-500">{message}</p>
                )}
            </div>
        </div>
    )
}

export default Authentication
