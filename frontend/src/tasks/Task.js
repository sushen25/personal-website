import { useState } from 'react'

export default function Task ({ task, handleTaskDelete, handleUpdateTask }) {
    const [isEditing, setIsEditing] = useState(false)
    const [value, setValue] = useState(task.text)

    const handleInputChange = (event) => {
        setValue(event.target.value)
    }

    const handleSave = (task, newValue) => {
        task.text = newValue
        handleUpdateTask(task)
        setIsEditing(false)
    }

    if (isEditing) {
        return (
            <>
                <input
                    type="text"
                    value={value}
                    onChange={handleInputChange}
                />
                <button onClick={() => handleSave(task, value)}>Save</button>
            </>
        )
    }

    return (
        <>
            <div>
                {task.id} - {task.text}
                <button onClick={() => setIsEditing(true)}>Edit</button>
                <button onClick={() => handleTaskDelete(task.id)}>Delete</button>
            </div>
        </>
    )
}
