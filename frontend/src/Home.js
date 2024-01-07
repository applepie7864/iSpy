import React from 'react'
import './index.css'

const Home = () => {
  return (
    <div className='w-screen h-screen flex flex-col items-center justify-center gap-8'>
        <div className='text-9xl text-yellow-600 title'>iSpy</div>
        <div className='font-light text-lg text-zinc-300 pt-2'>The next frontier in intelligent home security</div>
        <div className='text-m text-gray-800 -translate-y-full'>&copy; Rosanne & Annie</div>
    </div>
  )
}

export default Home
