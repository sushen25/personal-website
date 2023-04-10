import { useState } from 'react'

export default function TaskAdd ({ handleAddTask }) {
    const [value, setValue] = useState('')

    const handleInputChange = (event) => {
        setValue(event.target.value)
    }

    const handleSubmit = (event) => {
        event.preventDefault()
        handleAddTask(value)
        setValue('')
    }

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={value}
                onChange={handleInputChange}
            />
            <button type="submit">Add</button>
        </form>
    )
}
