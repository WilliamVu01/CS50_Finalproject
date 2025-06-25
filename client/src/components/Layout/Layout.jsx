// client/src/components/Layout/Layout.jsx
import React from 'react';
import { Outlet } from 'react-router-dom'; // <--- IMPORT OUTLET HERE
import Navbar from './Navbar'; 

function Layout() { 
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 flex flex-col items-center w-full">
      <Navbar /> 
      <main className="flex-grow w-full max-w-7xl mx-auto p-4">
        <Outlet /> {/* <--- RENDER THE OUTLET HERE INSTEAD OF {children} */}
      </main>
    </div>
  );
}
export default Layout;