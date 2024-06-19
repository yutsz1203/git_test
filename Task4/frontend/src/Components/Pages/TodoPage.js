import React, {useState, useEffect} from 'react';
import {Card} from '../Card/card';
import {Form} from '../Form/form';

export const TodoPage = ()=> {
    const [todo, setTodo] = useState([])
    const [addTodo, setAddTodo] = useState('')

    useEffect(()=>{
        fetch('/api/task').then(response => {
            if(response.ok){
                return response.json()
            }
        }).then(data => setTodo(data))
            
    }, [])
    
    const handleFormChange = (inputValue) =>{
        setAddTodo(inputValue)
    }

    const handleFormSubmit = () => {
        fetch('/api/task', {
            method: 'POST',
            body: JSON.stringify({
                task_detail: addTodo
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        })
    }
    return (
        <>
            <h1>To-Do List Service</h1>
            <Form userInput={addTodo} onFormChange={handleFormChange} onFormSubmit={handleFormSubmit}/>
            <Card listOfTodos={todo}/>
        </>
    )
}