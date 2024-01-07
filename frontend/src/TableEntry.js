import React from 'react'

const TableEntry = ( {person, id} ) => {
    const name = person.fname + " " + person.lname;
    return (
        <tr>  
            <td className='px-6 py-4 text-center border-solid border-gray-900 border-2'>{ id }</td>
            <td className='px-6 py-4 text-left border-solid border-gray-900 border-2'>{ name }</td>
            <td className='px-6 py-4 text-left border-solid border-gray-900 border-2'>{ person.email }</td>
            <td className='px-6 py-4 text-left border-solid border-gray-900 border-2'>{ person.location }</td>
            <td className='px-6 py-4 text-left border-solid border-gray-900 border-2'>{ person.occupation }</td>
            <td className='px-6 py-4 text-center border-solid border-gray-900 border-2'>{ person.num_images }</td>
        </tr>
    )
}

export default TableEntry
