import React from 'react'
import Garbage from './assets/Garbage';

const EditTableEntry = ({ person, id }) => {
    const name = person.fname + " " + person.lname;
    return (
        <tr>  
            <td className='px-6 py-4 text-center border-solid border-gray-900 border-2'>{ id }</td>
            <td className='px-6 py-4 text-left border-solid border-gray-900 border-2'>{ name }</td>
            <td className='px-6 py-4 text-left border-solid border-gray-900 border-2'>
                <input type='text' placeholder={ person.email } className='px-2 py-1 w-40 bg-zinc-300 text-gray-600 placeholder:text-gray-600' />
            </td>
            <td className='px-6 py-4 text-left border-solid border-gray-900 border-2'>
                <input type='text' placeholder={ person.location } className='px-2 py-1 w-40 bg-zinc-300 text-gray-600 placeholder:text-gray-600' />
            </td>
            <td className='px-6 py-4 text-left border-solid border-gray-900 border-2'>
                <input type='text' placeholder={ person.occupation } className='px-2 py-1 w-40 bg-zinc-300 text-gray-600 placeholder:text-gray-600' />
            </td>
            <td className='px-6 py-4 text-center border-solid border-gray-900 border-2'>
                <input type="file" id="files" name="files" multiple className='w-56 file:cursor-pointer text-zinc-300 text-xs leading-6 file:text-gray-600 file:font-semibold file:border-none file:px-4 file:py-1 hover:file:bg-gray-900 border border-zinc-300' />
            </td>
            <td className='px-6 py-4 border-solid border-gray-900 border-2'><div className='translate-x-1/4 cursor-pointer hover:origin-left hover:scale-110'><Garbage></Garbage></div></td>
        </tr>
    )
}

export default EditTableEntry
