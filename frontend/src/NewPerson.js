import React from 'react'

const NewPerson = () => {
    const handleSubmit = async (e) => {
        e.preventDefault();
        var msg = document.getElementsByClassName("message")[0];
        msg.innerHTML = "Adding user and updating the model ..."
        const form = document.getElementById('add_form');
        const formData = new FormData(form);
        try {
            const response = await fetch('http://127.0.0.1:5000/add_user', {
                method: 'POST',
                body: formData
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            } else {
                console.log('Data successfully sent to the API');
            }
        } catch (err) {
            console.error('Error sending data to the API:', err.message);
        }
        window.location.href = "http://localhost:3000/dataset";
    }

    return (
        <div className='w-screen h-screen flex flex-col items-center justify-center'>
            <h1 className='text-yellow-600 text-xl pb-2'>Add a Person to the Dataset!</h1>
            <form onSubmit={ handleSubmit } id="add_form" className='flex flex-col'>
                <div className='text-sm'>First Name:</div>
                <input type="text" id="fname" name="fname" className='mb-3 px-2 w-80 bg-zinc-300 text-gray-800 placeholder:text-gray-600' />
                <div className='text-sm'>Last Name:</div>
                <input type="text" id="lname" name="lname" className='mb-3 px-2 w-80 bg-zinc-300 text-gray-800 placeholder:text-gray-600' />
                <div className='text-sm'>Location:</div>
                <input type="text" id="location" name="location" className='mb-3 px-2 w-80 bg-zinc-300 text-gray-800 placeholder:text-gray-600' />
                <div className='text-sm'>Occupation:</div>
                <input type="text" id="occupation" name="occupation" className='mb-3 px-2 w-80 bg-zinc-300 text-gray-800 placeholder:text-gray-600' />
                <div className='text-sm'>Email:</div>
                <input type="text" id="email" name="email" className='mb-3 px-2 w-80 bg-zinc-300 text-gray-800 placeholder:text-gray-600' />
                <div className='text-sm'>Images:</div>
                <input type="file" multiple id="images" name="images" accept=".jpg, .jpeg, .png" className='text-sm mb-5'/>
                <button type="submit" className="w-20 mb-5 py-2 px-2 flex items-center justify-center flex text-sm rounded-sm border border-gray-600 text-gray-600 hover:border-yellow-600 hover:text-yellow-600">Submit</button>
                <div className='message text-zinc-300 text-sm'></div>
            </form>
        </div>
    )
}

export default NewPerson
