import React from 'react'

const AlertPopup = ({ message, type, onClose }) => {
    const alertStyles = {
        success: 'bg-green-500',
        error: 'bg-red-500',
        warning: 'bg-yellow-500',
        info: 'bg-blue-500'
    }

    return (
        <div
            className={`fixed top-0 right-0 m-4 p-4 rounded-lg text-white shadow-lg ${
                alertStyles[type] || alertStyles.info
            }`}
            role="alert"
        >
            <div className="relative">
                <span className="block sm:inline pr-8">{message}</span>
                <button
                    className="absolute top-0 bottom-0 right-0 px-3 text-2xl font-bold leading-none"
                    onClick={onClose}
                >
          &times;
                </button>
            </div>
        </div>
    )
}

export default AlertPopup
