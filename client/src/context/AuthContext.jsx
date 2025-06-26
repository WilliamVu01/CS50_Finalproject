// src/context/AuthContext.jsx
import React, { useState, useEffect, createContext, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import apiService from '../services/api'; // Correct default import for the apiService object

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); // Stores user object if logged in
  const [isAuthReady, setIsAuthReady] = useState(false); // Indicates if initial auth check is done
  const navigate = useNavigate();

  // Helper functions for API calls, now directly using methods from the imported 'apiService' object.
  // These are *not* performing the raw axios calls themselves, but calling the functions
  // defined in api.jsx (which then use the internal axios 'api' instance).
  const performLogin = async (email, password) => {
    try {
      const response = await apiService.loginUser(email, password);
      // apiService.loginUser already returns response.data
      // Backend returns { message: "...", user: { id: ..., firstName: ..., role: ... } }
      return response;
    } catch (error) {
      throw error;
    }
  };

  const performRegister = async (userData) => {
    try {
      const response = await apiService.registerUser(userData);
      // apiService.registerUser already returns response.data
      // Backend returns { message: "...", user: { id: ..., firstName: ..., role: ... } }
      return response;
    } catch (error) {
      throw error;
    }
  };

  const performLogout = async () => {
    try {
      const response = await apiService.logoutUser();
      return response;
    } catch (error) {
      throw error;
    }
  };

  const performGetCurrentUser = async () => {
    try {
      // apiService.getCurrentUser directly returns the serialized user object
      // Backend returns { id: ..., firstName: ..., role: ... } directly for /current_user
      const currentUser = await apiService.getCurrentUser();
      return currentUser;
    } catch (error) {
      throw error;
    }
  };

  // On initial load, try to fetch current user (check existing session)
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const currentUserData = await performGetCurrentUser(); // This directly returns serialized user obj
        console.log("Initial auth check: current user data:", currentUserData); // Debug log
        if (currentUserData && currentUserData.id) { // Check if a valid user object was returned
          setUser(currentUserData); // Set the user directly from the response
        } else {
          setUser(null); // No current user found or invalid data
        }
      } catch (error) {
        console.error("Initial auth check error:", error); // Debug log
        setUser(null);
      } finally {
        setIsAuthReady(true);
      }
    };
    checkAuth();
  }, []); // Run only once on component mount

  const login = async (email, password) => {
    try {
      const data = await performLogin(email, password); // data is { message: "...", user: {...} }
      console.log("Login successful, received data:", data); // Debug log
      setUser(data.user); // Access the 'user' key from the response
      toast.success(data.message);
      navigate('/');
    } catch (error) {
      console.error("Login error:", error); // Debug log
      toast.error(error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      const data = await performLogout();
      setUser(null);
      toast.success(data.message);
      navigate('/login');
    } catch (error) {
      console.error("Logout error:", error); // Debug log
      toast.error(error);
      throw error;
    }
  };

  const register = async (userData) => {
    try {
      const data = await performRegister(userData); // data is { message: "...", user: {...} }
      console.log("Register successful, received data:", data); // Debug log
      setUser(data.user); // Set the user after successful registration and login (assuming backend logs in user)
      toast.success(data.message);
      navigate('/'); // MINIMUM CHANGE: Changed from '/login' to '/' (assuming auto-login after register)
      // If backend doesn't auto-login, keep '/login' and user won't be set until explicit login
    } catch (error) {
      console.error("Register error:", error); // Debug log
      toast.error(error);
      throw error;
    }
  };

  const authContextValue = {
    user,
    isLoggedIn: !!user,
    isAuthReady,
    login,
    logout,
    register,
  };

  return (
    <AuthContext.Provider value={authContextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
