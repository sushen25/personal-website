import { useState } from 'react'
import TaskAdd from './TaskAdd'
import TasksList from './TasksList'

export default function TasksApp() {
    const [id, setId] = useState(1);
    const [tasks, setTasks] = useState([]);

    function getNextId() {
        setId(id + 1);
        return id;
    }

    function handleAddTask(text) {
        setTasks([
            ...tasks,
            {
                id: getNextId(),
                text: text,
            }
        ])
    }

    function handleUpdateTask(task) {
        setTasks(
            tasks.map((t) => {
                if (t.id === task.id) {
                return task;
                } else {
                return t;
                }
            })
        );
    }

    function handleDeleteTask(taskId) {
        setTasks(tasks.filter((t) => t.id !== taskId));
    }

    

    return (
        <>
            <h1>TODO List</h1>
            <TaskAdd handleAddTask={handleAddTask}/>
            <TasksList tasks={tasks} handleTaskDelete={handleDeleteTask} handleUpdateTask={handleUpdateTask}/>
        </>
    );
}