import React, { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext()

export const useAuth = () => {
    return useContext(AuthContext)
}

export const AuthProvider = ({ children }) => {
    const [authenticated, setAuthenticated] = useState(false)
    const [username, setUsername] = useState('')

    useEffect(() => {
        const storedAuth = localStorage.getItem('authenticated')
        const storedUsername = localStorage.getItem('username')
        const storedExpirationTime = localStorage.getItem('expirationTime')

        if (storedAuth && storedUsername && storedExpirationTime && Date.now() < JSON.parse(storedExpirationTime)) {
            setAuthenticated(JSON.parse(storedAuth))
            setUsername(storedUsername)
        } else {
            localStorage.removeItem('authenticated')
            localStorage.removeItem('username')
            localStorage.removeItem('expirationTime')
        }
    }, [])

    const login = (user) => {
        setUsername(user)
        setAuthenticated(true)
        localStorage.setItem('authenticated', JSON.stringify(true))
        localStorage.setItem('username', user)

        const expirationTime = Date.now() + 1000 * 60 * 60
        localStorage.setItem('expirationTime', JSON.stringify(expirationTime))
    }

    const logout = () => {
        setUsername('')
        setAuthenticated(false)
        localStorage.setItem('authenticated', JSON.stringify(false))
        localStorage.setItem('username')
    }

    const value = {
        authenticated,
        username,
        login,
        logout
    }

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
