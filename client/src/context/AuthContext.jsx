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
      const response = await apiService.loginUser(email, password); // Use apiService.loginUser
      return response; // apiService.loginUser already returns response.data
    } catch (error) {
      throw error; // apiService.loginUser already throws the message
    }
  };

  const performRegister = async (userData) => {
    try {
      const response = await apiService.registerUser(userData); // Use apiService.registerUser
      return response; // apiService.registerUser already returns response.data
    } catch (error) {
      throw error; // apiService.registerUser already throws the message
    }
  };

  const performLogout = async () => {
    try {
      const response = await apiService.logoutUser(); // Use apiService.logoutUser
      return response; // apiService.logoutUser already returns response.data
    } catch (error) {
      throw error; // apiService.logoutUser already throws the message
    }
  };

  const performGetCurrentUser = async () => {
    try {
      const currentUser = await apiService.getCurrentUser(); // Use apiService.getCurrentUser
      return currentUser; // apiService.getCurrentUser already returns user object or null
    } catch (error) {
      throw error; // apiService.getCurrentUser already throws the message
    }
  };

  // On initial load, try to fetch current user (check existing session)
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const currentUser = await performGetCurrentUser(); // Use the internal helper
        if (currentUser) {
          setUser(currentUser.user || currentUser); // Adjust based on if backend wraps user in 'user' key
        }
      } catch (error) {
        // Error already logged by performGetCurrentUser or handled by toast if re-thrown
        setUser(null);
      } finally {
        setIsAuthReady(true);
      }
    };
    checkAuth();
  }, []); // Run only once on component mount

  const login = async (email, password) => {
    try {
      const data = await performLogin(email, password);
      setUser(data.user); // Assuming loginUser returns { user: {...}, message: "..." }
      toast.success(data.message);
      navigate('/'); // MINIMUM CHANGE: Changed from '/dashboard' to '/'
    } catch (error) {
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
      toast.error(error);
      throw error;
    }
  };

  const register = async (userData) => {
    try {
      const data = await performRegister(userData);
      toast.success(data.message);
      navigate('/login');
    } catch (error) {
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