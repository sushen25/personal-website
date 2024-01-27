import Modal from 'react-modal'

Modal.setAppElement('#root')

const FeaturedProjectModal = ({ isOpen, onRequestClose, contentLabel, children }) => {
    return (
        <Modal
            isOpen={isOpen}
            onRequestClose={onRequestClose}
            contentLabel={contentLabel}
            style={{
                overlay: {
                    background: 'rgba(0, 0, 0, 0.5)'
                },
                content: {
                    width: '80%', // Adjust the width as needed
                    maxWidth: '800px',
                    margin: 'auto',
                    maxHeight: '80%', // Set a maximum height for the modal content
                    overflow: 'auto' // Enable scrolling if content overflows
                }
            }}
        >
            {children}
        </Modal>
    )
}

export default FeaturedProjectModal
