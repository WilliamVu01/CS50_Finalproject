// client/src/services/api.jsx
import axios from 'axios';

// Helper function to transform object keys from camelCase to snake_case for backend
const toSnakeCase = (obj) => {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }
  if (Array.isArray(obj)) {
    return obj.map(toSnakeCase);
  }
  return Object.keys(obj).reduce((acc, key) => {
    const snakeKey = key.replace(/([A-Z])/g, '_$1').toLowerCase();
    acc[snakeKey] = toSnakeCase(obj[key]);
    return acc;
  }, {});
};

// Helper function to transform object keys from snake_case to camelCase for frontend
const toCamelCase = (obj) => {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }
  if (Array.isArray(obj)) {
    return obj.map(toCamelCase);
  }
  return Object.keys(obj).reduce((acc, key) => {
    const camelKey = key.replace(/_([a-z])/g, (g) => g[1].toUpperCase());
    acc[camelKey] = toCamelCase(obj[key]);
    return acc;
  }, {});
};


// Create an Axios instance with credentials for session cookies
const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  withCredentials: true, // Important for sending/receiving session cookies with Flask-Login
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Add a request interceptor to transform outgoing data to snake_case
api.interceptors.request.use(
  (config) => {
    if (config.data) {
      config.data = toSnakeCase(config.data);
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add a response interceptor to transform incoming data to camelCase
api.interceptors.response.use(
  (response) => {
    if (response.data) {
      response.data = toCamelCase(response.data);
    }
    return response;
  },
  (error) => {
    // Error handling logic
    let errorMessage = 'An unexpected error occurred.';
    if (error.response) {
      // Server responded with a status other than 2xx
      console.error('API Error Response:', error.response.data);
      console.error('Status:', error.response.status);
      console.error('Headers:', error.response.headers);
      errorMessage = error.response.data.message || error.response.data.error || errorMessage;
      if (error.response.status === 401) {
        errorMessage = errorMessage || 'Unauthorized: Login required.';
      } else if (error.response.status === 403) {
        errorMessage = errorMessage || 'Forbidden: You do not have permission to perform this action.';
      } else if (error.response.status === 400) {
        errorMessage = errorMessage || 'Bad Request: Please check your input.';
      } else if (error.response.status === 409) {
        errorMessage = errorMessage || 'Conflict: Resource already exists or conflict occurred.';
      }
    } else if (error.request) {
      // Request was made but no response received
      console.error('API Error Request:', error.request);
      errorMessage = 'No response from server. Please check your internet connection or server status.';
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('API Error Message:', error.message);
      errorMessage = error.message;
    }
    // Propagate the error message for toast notifications in components
    return Promise.reject(errorMessage);
  }
);


// Define API service methods
const apiService = {
  // Auth Endpoints
  loginUser: async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    return response.data; // Return data directly, it's already camelCase
  },

  registerUser: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data; // Return data directly, it's already camelCase
  },

  logoutUser: async () => {
    const response = await api.post('/auth/logout');
    return response.data; // Return data directly
  },

  getCurrentUser: async () => {
    try {
      const response = await api.get('/auth/current_user');
      return response.data; // This should return the user object or null
    } catch (error) {
      // If 401 on current_user, it means not logged in, which is expected behavior for this endpoint
      console.warn("getCurrentUser failed, likely not logged in:", error);
      return null; // Return null if not logged in
    }
  },

  // User Management
  getUsers: async () => {
    const response = await api.get('/users');
    return response.data;
  },
  getUser: async (id) => {
    const response = await api.get(`/users/${id}`);
    return response.data;
  },
  updateUser: async (id, userData) => {
    const response = await api.put(`/users/${id}`, userData);
    return response.data;
  },
  deleteUser: async (id) => {
    const response = await api.delete(`/users/${id}`);
    return response.data;
  },

  // Training Element Management
  getTrainingElements: async () => {
    const response = await api.get('/training_elements');
    return response.data;
  },
  getTrainingElement: async (id) => {
    const response = await api.get(`/training_elements/${id}`);
    return response.data;
  },
  createTrainingElement: async (elementData) => {
    const response = await api.post('/training_elements', elementData);
    return response.data;
  },
  updateTrainingElement: async (id, elementData) => {
    const response = await api.put(`/training_elements/${id}`, elementData);
    return response.data;
  },
  deleteTrainingElement: async (id) => {
    const response = await api.delete(`/training_elements/${id}`);
    return response.data;
  },
  // NEW: Method to fetch allowed session types
  getTrainingSessionTypes: async () => {
    const response = await api.get('/training_elements/session_types');
    return response.data; // This should be an array of strings
  },

  // Booking Management
  getBookings: async () => {
    const response = await api.get('/bookings');
    return response.data;
  },
  getBooking: async (id) => {
    const response = await api.get(`/bookings/${id}`);
    return response.data;
  },
  createBooking: async (bookingData) => {
    const response = await api.post('/bookings', bookingData);
    return response.data;
  },
  updateBooking: async (id, bookingData) => {
    const response = await api.put(`/bookings/${id}`, bookingData);
    return response.data;
  },
  deleteBooking: async (id) => {
    const response = await api.delete(`/bookings/${id}`);
    return response.data;
  },
};

export default apiService;
