import React, { useState, useEffect } from 'react'
import axios from 'axios';
import TableEntry from './TableEntry';
import { Link } from 'react-router-dom';

const Dataset = () => {
    const [data, setData] = useState([]);
    const getData = async () => {
        try {
            const response = await axios.get('http://localhost:5000/all_users');
            setData(response.data);
        } catch (error) {
            console.error('There was a problem with the GET request:', error);
        }
    };
    useEffect(() => {
        getData();
    }, [])
    if (data.length !== 0) {
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
                            <th className='px-6 py-4 border-solid border-gray-900 border-2 text-center'>No. Images</th>
                        </tr>
                        {data && data.map((person, id) => {
                            return <TableEntry person={person} id={id} />
                        })}
                    </tbody>
                    <div className='w-14 text-center p-2 underline hover:no-underline cursor-pointer'>
                        <Link to='/edit_db' state={ data }>Edit</Link>
                    </div>
                </table>
            </div>
        )
    } else {
        return (
            <div className='font-light text-lg w-screen h-screen flex flex-col items-center justify-center text-zinc-600'>Unable to fetch data.</div>
        )
    }
}

export default Dataset
