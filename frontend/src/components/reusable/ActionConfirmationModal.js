import Modal from 'react-modal'

function ActionConfirmationModal ({ confirmationTitle, confirmationText, isOpen, onClose, onConfirm }) {
    confirmationTitle = confirmationTitle || 'Confirm Action'
    confirmationText = confirmationText || 'Are you sure you want to perform this action?'

    const modalStyle = {
        content: {
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            maxWidth: '400px',
            width: '100%',
            height: '200px',
            padding: '20px',
            textAlign: 'left'
        },
        overlay: {
            backgroundColor: 'rgba(0, 0, 0, 0.7)'
        }
    }

    const buttonContainerStyle = {
        display: 'flex',
        justifyContent: 'flex-end', // Align buttons to the right
        marginTop: '50px' // Add some space between buttons and content
    }

    return (
        <Modal
            isOpen={isOpen}
            onRequestClose={onClose}
            contentLabel="Action Confirmation Modal"
            style={modalStyle}
        >
            <h2 className='text-xl'>Confirm Action</h2>
            <p className='text-md'>{confirmationText}</p>
            <div style={buttonContainerStyle}>
                <button
                    className='py-1 px-2 mr-3 bg-gray-600 text-white font-semibold rounded hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-opacity-75'
                    onClick={onClose}>
                        Cancel
                </button>
                <button
                    className='py-1 px-2 mr-3 bg-red-600 text-white font-semibold rounded hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-opacity-75'
                    onClick={onConfirm}>
                        Confirm
                </button>
            </div>
        </Modal>
    )
}

export default ActionConfirmationModal
