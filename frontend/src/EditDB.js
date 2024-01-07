import React from 'react'
import { useLocation } from 'react-router-dom'
import EditTableEntry from './EditTableEntry'
import { Link } from 'react-router-dom';

const EditDB = () => {
    const location = useLocation();
    const data = location.state;
    return (
        <div className='w-screen h-screen flex flex-col items-center justify-top py-28'>
            <table className='p-4 flex flex-col justify-center items-center w-11/12'>
                <tbody>
                    <tr className='bg-gray-900'>
                        <th className='px-6 py-4 border-solid border-gray-900 border-2 text-center'>ID</th>
                        <th className='px-6 py-4 border-solid border-gray-900 border-2 text-left'>Name</th>
                        <th className='px-6 py-4 border-solid border-gray-900 border-2 text-left'>Email</th>
                        <th className='px-6 py-4 border-solid border-gray-900 border-2 text-left'>Location</th>
                        <th className='px-6 py-4 border-solid border-gray-900 border-2 text-left'>Occupation</th>
                        <th className='px-6 py-4 border-solid border-gray-900 border-2 text-center'>Images</th>
                        <th className='px-6 py-4 border-solid border-gray-900 border-2 text-center'>Remove</th>
                    </tr>
                    {data && data.map((person, id) => {
                        return <EditTableEntry person={person} id={id} />
                    })}
                    <tr>
                        <td colSpan={7} className='py-0.5 text-gray-600 border-solid border-gray-900 border-2 text-center cursor-pointer hover:bg-gray-900'>+</td>
                    </tr>
                </tbody>
                <div className='w-14 text-center p-4 cursor-pointer flex flex-row items-center justify-center gap-8'>
                    <div className='underline hover:no-underline'>Save</div>
                    <div className='underline hover:no-underline'><Link to='/dataset'>Cancel</Link></div>
                </div>
            </table>
        </div>
    )
}

export default EditDB
