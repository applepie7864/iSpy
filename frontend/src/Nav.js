import React from 'react'
import Camera from './assets/Camera'
import Search from './assets/Search'
import { Link } from 'react-router-dom';

const Nav = () => {
    return (
        <nav className='fixed top-0 left-0 px-12 py-8 flex flex-row w-screen h-20 justify-between items-center'>
            <Search></Search>
            <div className='c w-4/12 flex flex-row justify-between items-center'>
                <div className='hover:text-gray-600'><Link to="/">Home</Link></div>
                <div className='hover:text-gray-600'><Link to="/dataset">Dataset</Link></div>
                <a className='hover:scale-105' href="http://localhost:5000/webcam"><Camera></Camera></a>
            </div>
        </nav>
    )
}

export default Nav
