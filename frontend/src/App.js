import React from 'react'
import Nav from "./Nav";
import { Routes, Route } from "react-router-dom";
import Home from './Home';
import Dataset from './Dataset';
import EditDB from './EditDB'

function App() {
	return (
		<div className="bg-gray-950 w-screen h-screen text-zinc-300 font-sans">
			<Nav></Nav>
			<Routes>
				<Route path="/" element={ <Home /> } />
				<Route path="/dataset" element={ <Dataset /> } />
				<Route path="/edit_db" element={ <EditDB /> } />
			</Routes>
		</div>
	);
}

export default App;
