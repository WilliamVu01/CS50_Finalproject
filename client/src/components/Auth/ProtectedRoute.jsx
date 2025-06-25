// client/src/components/ProtectedRoute.jsx
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import { useAuth } from '../../context/AuthContext'; // Correct relative import path

function ProtectedRoute({ children }) {
  const { isLoggedIn, isAuthReady } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    // Only navigate if auth check is complete and user is not logged in
    if (isAuthReady && !isLoggedIn) {
      navigate('/login', { replace: true });
      toast.error("You need to be logged in to view this page.");
    }
  }, [isLoggedIn, isAuthReady, navigate]);

  if (!isAuthReady) {
    // Show a loading spinner or message while authentication status is being determined
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
        <p className="ml-4 text-gray-700">Loading authentication...</p>
      </div>
    );
  }

  // If auth is ready and user is logged in, render the children
  return isLoggedIn ? children : null; // Return null if not logged in; navigation handles redirection
}

export default ProtectedRoute;
