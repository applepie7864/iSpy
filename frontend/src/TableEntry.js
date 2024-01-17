import React, { useEffect, useState } from 'react'
import Edit from './assets/Edit';

const TableEntry = ( {person, id} ) => {
    const form_id = "form_" + id;
    const name = person.fname + " " + person.lname;
    const [form, setForm] = useState(false)
    function editMode() {
        var edit = document.getElementById(id);
        setForm(true);
    }
    const [formChanges, setFormChanges] = useState({});
    const handleChange = (e) => {
        if (e.target.value !== "")
        {
            setFormChanges({
                ...formChanges,
                [e.target.name]: e.target.value
            });
        }
    };
    const handleSubmit = async (e) => {
        e.preventDefault();
        if(Object.keys(formChanges).length !== 0) {
            for (const key in formChanges) {
                if (formChanges[key] === "") {
                    continue;
                }
                const formData = new FormData();
                formData.append('fname', person.fname);
                formData.append('lname', person.lname);
                formData.append('option', key);
                formData.append('value', formChanges[key]);
                try {
                    const response = await fetch('http://127.0.0.1:5000/edit_user', {
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
            }
        }
        setForm(false);
        setFormChanges({})
    }
    if (!form) {
        return (
            <tr>  
                <td className='px-6 py-4 text-center border-solid border-gray-900 border-2'>{ id }</td>
                <td className='px-6 py-4 text-left border-solid border-gray-900 border-2'>{ name }</td>
                <td className='px-6 py-4 text-left border-solid border-gray-900 border-2'>{ person.email }</td>
                <td className='px-6 py-4 text-left border-solid border-gray-900 border-2'>{ person.location }</td>
                <td className='px-6 py-4 text-left border-solid border-gray-900 border-2'>{ person.occupation }</td>
                <td className='px-6 py-4 text-center border-solid border-gray-900 border-2'>{ person.num_images }</td>
                <div id={id} className="cursor-pointer pl-3 pt-4" onClick={editMode}><Edit /></div>
            </tr>
        )
    } else {
        return (
            <tr>  
                <form onSubmit={handleSubmit} id={form_id}></form>
                <td className='px-6 py-4 text-center border-solid border-gray-900 border-2'>{ id }</td>
                <td className='px-6 py-4 text-left border-solid border-gray-900 border-2'>{ name }</td>
                <td className='px-6 py-4 text-left border-solid border-gray-900 border-2'>
                    <input form={form_id} type='text' placeholder={ person.email } className='px-2 py-1 w-40 bg-zinc-300 text-gray-800 placeholder:text-gray-600' name="email" onChange={handleChange} />
                </td>
                <td className='px-6 py-4 text-left border-solid border-gray-900 border-2'>
                    <input form={form_id} type='text' placeholder={ person.location } className='px-2 py-1 w-40 bg-zinc-300 text-gray-800 placeholder:text-gray-600' name="location" onChange={handleChange} />
                </td>
                <td className='px-6 py-4 text-left border-solid border-gray-900 border-2'>
                    <input form={form_id} type='text' placeholder={ person.occupation } className='px-2 py-1 w-40 bg-zinc-300 text-gray-800 placeholder:text-gray-600' name="occupation" onChange={handleChange} />
                </td>
                <td className='px-6 py-4 text-center border-solid border-gray-900 border-2'>{ person.num_images }</td>
                <div id={id} className="cursor-pointer pl-2 pt-5"><button className="underline hover:no-underline" form={form_id} type='submit'>Save</button></div>
            </tr>
        )
    }
}

export default TableEntry
