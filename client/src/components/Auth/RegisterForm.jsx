// client/src/components/Auth/RegisterForm.jsx
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext'; // Correct relative import path

function RegisterForm() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    role: 'student', // Default role
  });
  const [isLoading, setIsLoading] = useState(false);
  const { register } = useAuth(); // Use the register function from AuthContext

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await register(formData);
      // Registration successful, navigate or show success message (handled by toast)
    } catch (error) {
      // Error message already handled by toast in AuthContext
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Register</h2>
        <div className="mb-4">
          <label htmlFor="email" className="block text-gray-700 text-sm font-bold mb-2 text-left">
            Email:
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="password" className="block text-gray-700 text-sm font-bold mb-2 text-left">
            Password:
          </label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="first_name" className="block text-gray-700 text-sm font-bold mb-2 text-left">
            First Name:
          </label>
          <input
            type="text"
            id="first_name"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            required
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="last_name" className="block text-gray-700 text-sm font-bold mb-2 text-left">
            Last Name:
          </label>
          <input
            type="text"
            id="last_name"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            required
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
        {/* Optional: Role selection for registration, if allowed. Otherwise, backend can default. */}
        <div className="mb-6">
          <label htmlFor="role" className="block text-gray-700 text-sm font-bold mb-2 text-left">
            Role:
          </label>
          <select
            id="role"
            name="role"
            value={formData.role}
            onChange={handleChange}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          >
            <option value="student">Student</option>
            <option value="instructor">Instructor</option>
            {/* <option value="admin">Admin</option> -- Keep admin role for backend assignment for security */}
          </select>
        </div>
        <button
          type="submit"
          className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-full focus:outline-none focus:shadow-outline w-full disabled:opacity-50"
          disabled={isLoading}
        >
          {isLoading ? 'Registering...' : 'Register'}
        </button>
        <p className="mt-4 text-center text-gray-600">
          Already have an account? <Link to="/login" className="text-green-500 hover:text-green-700">Login here</Link>
        </p>
      </form>
    </div>
  );
}

export default RegisterForm;
