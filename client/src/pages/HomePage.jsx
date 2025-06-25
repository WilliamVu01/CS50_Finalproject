// client/src/pages/HomePage.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // Correct relative import path

function HomePage() {
  const { isLoggedIn, user } = useAuth();

  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-64px)] bg-gradient-to-br from-blue-100 to-purple-90 text-gray-800 p-10 rounded-lg shadow-lg">
      <h1 className="text-5xl font-extrabold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 animate-fade-in">
        Welcome to Training Scheduler!
      </h1>
      <p className="text-xl mb-8 max-w-2xl text-center leading-relaxed">
        Your ultimate tool for managing training schedules, elements, and bookings efficiently.
        Get started by logging in or registering.
      </p>

      {!isLoggedIn && (
        <div className="flex flex-col sm:flex-row gap-4">
          <Link
            to="/login"
            className="bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold py-3 px-8 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 ease-in-out"
          >
            Login
          </Link>
          <Link
            to="/register"
            className="bg-gradient-to-r from-pink-500 to-orange-600 text-white font-semibold py-3 px-8 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 ease-in-out"
          >
            Register
          </Link>
        </div>
      )}
      {/* If logged in, Navbar already provides navigation to dashboard/logout */}
    </div>
  );
}

export default HomePage;
