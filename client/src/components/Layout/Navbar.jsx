import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import apiService from '../../services/api';
import { toast } from 'react-hot-toast';

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await apiService.logoutUser();
      logout();
      toast.success('Logged out successfully!');
      navigate('/login');
    } catch (error) {
      toast.error(error.message || 'Failed to logout.');
      console.error("Logout error:", error);
    }
  };

  return (
    <nav className="bg-gray-800 p-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        {/* Brand logo/name - links to the Calendar page (which is the index route) */}
        <Link to="/" className="text-white text-xl font-bold">
          Training Scheduler
        </Link>
        <div className="flex items-center space-x-4">
          {user ? (
            <>
              {/* Welcome message for logged-in users */}
              <span className="text-gray-300">Welcome, {user.first_name}! ({user.role})</span>

              {/* Navigation links for logged-in users */}
              <Link to="/home" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
                Home
              </Link>
              <Link to="/dashboard" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
                Dashboard
              </Link>
              <Link to="/" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
                Calendar
              </Link>
              
              {/* Conditional link for Manage Elements (Admin/Instructor roles) */}
              {(user.role === 'admin' || user.role === 'instructor') && (
                <Link to="/manage-elements" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
                  Manage Elements
                </Link>
              )}

              {/* Logout button */}
              <button
                onClick={handleLogout}
                className="bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-md text-sm font-medium transition duration-300"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              {/* Navigation links for non-logged-in users */}
              <Link to="/login" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
                Login
              </Link>
              <Link to="/register" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;