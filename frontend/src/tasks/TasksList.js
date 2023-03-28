import Task from "./Task";

export default function TasksList({ tasks, handleTaskDelete, handleUpdateTask }) {

    function getTasks() {
        if (tasks) {
            return tasks.map((task) => {
                return (
                    <Task key={task.id} task={task} handleTaskDelete={handleTaskDelete} handleUpdateTask={handleUpdateTask} />
                )
            });
        }
    }

    return (
        <>
            { getTasks() }
        </>
    );
}