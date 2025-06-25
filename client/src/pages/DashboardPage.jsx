// client/src/pages/DashboardPage.jsx
import React from 'react';
import { useAuth } from '../context/AuthContext'; // Correct relative import path

function DashboardPage() {
  const { user } = useAuth(); // Access user from AuthContext

  if (!user) {
    // This case should ideally be handled by ProtectedRoute, but good for defensive coding
    return <div className="text-center text-lg text-gray-600">Loading user data...</div>;
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-64px)] bg-gradient-to-br from-green-50 to-blue-100 p-6 rounded-lg shadow-lg">
      <div className="bg-white p-10 rounded-xl shadow-2xl transform transition-all duration-300 hover:scale-105 w-full max-w-2xl text-center">
        <h2 className="text-4xl font-extrabold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-green-700 to-teal-700">
          Welcome to Your Dashboard!
        </h2>
        <div className="text-left text-lg space-y-3 mb-8">
          <p>
            <span className="font-semibold text-gray-700">Email:</span> <span className="text-blue-600">{user.email}</span>
          </p>
          <p>
            <span className="font-semibold text-gray-700">Name:</span> <span className="text-purple-600">{user.firstName} {user.lastName}</span>
          </p>
          <p>
            <span className="font-semibold text-gray-700">Role:</span> <span className="text-orange-600">{user.role}</span>
          </p>
          <p>
            <span className="font-semibold text-gray-700">User ID:</span> <span className="text-gray-500 break-words">{user.id}</span>
          </p>
        </div>
      </div>
    </div>
  );
}

export default DashboardPage;