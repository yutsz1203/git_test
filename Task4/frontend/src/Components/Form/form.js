import React from "react";

export const Form = ( { userInput , onFormChange, onFormSubmit} )=> {

    const handleChange = (event) => {
        onFormChange(event.target.value)
    }

    const handleSubmit = (event) => {
        onFormSubmit()
    }
    return (
    <>
        <form onSubmit={handleSubmit}>
            <input type='text' required value={userInput} onChange={handleChange} placeholder="Input a new to-do"></input>
            <input type='submit' class='addButton' value='Add'></input>
        </form>
    </>
    )
} 