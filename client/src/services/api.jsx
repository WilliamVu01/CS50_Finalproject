import axios from 'axios';

// Create an Axios instance with credentials for session cookies
const api = axios.create({
  baseURL: 'http://localhost:5000/api', // IMPORTANT: Ensure this matches your Flask backend URL
  withCredentials: true, // Important for sending/receiving session cookies with Flask-Login
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Helper function to transform camelCase keys (from backend responses) to snake_case for frontend consistency
const toSnakeCase = (obj) => {
  if (obj === null || typeof obj !== 'object' || obj instanceof Date) {
    return obj;
  }
  if (Array.isArray(obj)) {
    return obj.map(v => toSnakeCase(v));
  }
  return Object.keys(obj).reduce((acc, key) => {
    const snakeKey = key.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);
    acc[snakeKey] = toSnakeCase(obj[key]);
    return acc;
  }, {});
};


const apiService = {
  // --- Authentication API functions ---
  loginUser: async (email, password) => {
    try {
      const response = await api.post('/auth/login', { email, password });
      return response.data;
    } catch (error) {
      throw error.response?.data?.message || 'Login failed';
    }
  },

  registerUser: async (userData) => {
    try {
      const response = await api.post('/auth/register', userData);
      return response.data;
    } catch (error) {
      throw error.response?.data?.message || 'Registration failed';
    }
  },

  logoutUser: async () => {
    try {
      const response = await api.post('/auth/logout');
      return response.data;
    } catch (error) {
      throw error.response?.data?.message || 'Logout failed';
    }
  },

  getCurrentUser: async () => {
    try {
      const response = await api.get('/auth/current_user');
      return response.data;
    } catch (error) {
      if (error.response && error.response.status === 401) {
        return null;
      }
      console.error("Error fetching current user:", error);
      throw error.response?.data?.message || 'Failed to fetch current user';
    }
  },

  // --- Bookings API functions ---
  getBookings: async (params = {}) => {
    try {
      const response = await api.get('/bookings', { params: params });
      return response.data.map(booking => toSnakeCase(booking));
    } catch (error) {
      throw error.response?.data?.message || 'Failed to fetch bookings';
    }
  },

  createBooking: async (bookingData) => {
    try {
      const response = await api.post('/bookings', bookingData);
      return response.data;
    } catch (error) {
      throw error.response?.data?.message || 'Failed to create booking';
    }
  },

  updateBooking: async (bookingId, bookingData) => {
    try {
      const response = await api.put(`/bookings/${bookingId}`, bookingData);
      return response.data;
    } catch (error) {
      throw error.response?.data?.message || 'Failed to update booking';
    }
  },

  deleteBooking: async (bookingId) => {
    try {
      const response = await api.delete(`/bookings/${bookingId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data?.message || 'Failed to delete booking';
    }
  },

  // --- Users API functions (for dropdowns) ---
  getUsers: async (params = {}) => {
    try {
      const response = await api.get('/users', { params: params });
      return response.data.map(user => toSnakeCase(user));
    } catch (error) {
      throw error.response?.data?.message || 'Failed to fetch users';
    }
  },

  // --- Training Elements API functions ---
  getTrainingElements: async (params = {}) => {
    try {
      const response = await api.get('/training-elements', { params: params });
      return response.data.map(element => toSnakeCase(element));
    } catch (error) {
      throw error.response?.data?.message || 'Failed to fetch training elements';
    }
  },

  createTrainingElement: async (elementData) => {
    try {
      const response = await api.post('/training-elements', elementData);
      return response.data;
    } catch (error) {
      throw error.response?.data?.message || 'Failed to create training element';
    }
  },

  updateTrainingElement: async (elementId, elementData) => {
    try {
      const response = await api.put(`/training-elements/${elementId}`, elementData);
      return response.data;
    } catch (error) {
      throw error.response?.data?.message || 'Failed to update training element';
    }
  },

  deleteTrainingElement: async (elementId) => {
    try {
      const response = await api.delete(`/training-elements/${elementId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data?.message || 'Failed to delete training element';
    }
  },
};

export default apiService;