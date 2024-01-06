import React from 'react'
import Link from 'next/link'
import EyeIcon from '@/app/svgs/eye'

export default function NavBar() {
    return (
        <div>
            <div className='navBar'>
                <div className="left">
                    <div className="logo"><Link href="/"><EyeIcon /></Link></div>
                </div>
                <div className="right">
                    <div className="home"><Link href="/">Home</Link></div>
                    <div className="upload"><Link href="/db">Database</Link></div>
                </div>
            </div>
        </div>
    );
}