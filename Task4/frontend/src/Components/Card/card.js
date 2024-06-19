import React, { useState } from 'react';
import { Checkbox } from '../Checkbox/checkbox';

export const Card = ({ listOfTodos})=> {
    const [editingTaskId, setEditingTaskId] = useState(null);
    const [editedTaskDetail, setEditedTaskDetail] = useState("");

    const [deletingTaskId, setDeletingTaskId] = useState(null);

    const handleEditClick = (task) => {
        setEditingTaskId(task.task_id);
        setEditedTaskDetail(task.task_detail);
        
    };

    const handleEditChange = (event) => {
        setEditedTaskDetail(event.target.value);
    };

    const handleEditSubmit = async (task_id) => {

        const response = await fetch(`/api/task/${task_id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task_detail: editedTaskDetail })
        });

        if (response.ok) {
            const updatedTodos = listOfTodos.map(todo =>
                todo.task_id === task_id ? { ...todo, task_detail: editedTaskDetail } : todo
            );
            setEditingTaskId(null);
        } else {
            console.error('Failed to update the task');
        }

        window.location.reload();

    };

    const handleDeleteSubmit = async (task, task_id) => {
        setDeletingTaskId(task.task_id);

        const response = await fetch(`/api/task/${task.task_id}`, {
            method: 'DELETE',
            header: {
                'Accept': 'application/json',
                'Content-Type' : 'application/json',
            }
        });
        

        if (response.ok) {
            const updatedTodos = listOfTodos.filter(todo => todo.task_id !== task_id); 
            setDeletingTaskId(null);
        } else {
            console.error('Failed to delete the task');
        }
        
        window.location.reload();

    };

    const handleKeyDown = (e, task_id) => {
        if (e.key === 'Enter') {
            e.preventDefault(); 
            handleEditSubmit(task_id);
        }
    };
    
    return (
        <>
            <ul>
                {listOfTodos.map(todo => {
                    return (
                        <li key={todo.task_id} style={{ textDecoration: todo.done ? "line-through" : null }}>
                            <Checkbox
                                defaultChecked={todo.done}
                            />{" "}

                            {editingTaskId === todo.task_id ? (
                                <>
                                    <input
                                        type="text"
                                        value={editedTaskDetail}
                                        onChange={handleEditChange}
                                        onKeyDown={(e) => handleKeyDown(e, todo.task_id)}
                                    />
                                    <button onClick={() => handleEditSubmit(todo.task_id)}>Save</button>
                                    <button onClick={() => setEditingTaskId(null)}>Cancel</button>
                                </>
                            ) : (
                                <>
                                    {todo.task_detail}
                                    <button onClick={() => handleEditClick(todo)}>Edit</button>
                                    <button onClick={() => handleDeleteSubmit(todo,todo.task_id)}>Delete</button>
                                </>
                            )}
                        </li>
                    );
                })}
            </ul>
        </>
    );
}