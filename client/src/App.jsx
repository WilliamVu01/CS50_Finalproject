import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

// Imports based on the ABSOLUTE LATEST project structure confirmed by ALL provided images

// From components/Layout/ directory:
import Layout from './components/Layout/Layout'; // Path: client/src/components/Layout/Layout.jsx

// From components/Auth/ directory:
import ProtectedRoute from './components/Auth/ProtectedRoute'; // Path: client/src/components/Auth/ProtectedRoute.jsx

// From context/ directory:
import { AuthProvider } from './context/AuthContext'; // Path: client/src/context/AuthContext.jsx

// From pages/ directory:
import CalendarPage from './pages/CalendarPage'; // Path: client/src/pages/CalendarPage.jsx
import LoginPage from './pages/LoginPage';     // Path: client/src/pages/LoginPage.jsx
import RegisterPage from './pages/RegisterPage'; // Path: client/src/pages/RegisterPage.jsx
import TrainingElementManagement from './pages/TrainingElementManagement'; // Path: client/src/pages/TrainingElementManagement.jsx
import DashboardPage from './pages/DashboardPage'; // <--- ADD THIS IMPORT!
import HomePage from './pages/HomePage';         // <--- ADD THIS IMPORT!

function App() {
  return (
    <BrowserRouter>
      {/* AuthProvider wraps the entire application to provide authentication context */}
      <AuthProvider>
        {/* Toaster for displaying notifications (e.g., success/error messages) */}
        <Toaster position="top-right" reverseOrder={false} />

        <Routes>
          {/* Public routes (no authentication required) */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected routes wrapped by Layout */}
          {/* The Layout component will render the Navbar and an Outlet for nested routes */}
          <Route path="/" element={<Layout />}>
            {/* Index route for the root path '/', requires authentication */}
            <Route index element={<ProtectedRoute><CalendarPage /></ProtectedRoute>} />
            
            {/* Route for managing training elements, requires authentication */}
            <Route path="/manage-elements" element={<ProtectedRoute><TrainingElementManagement /></ProtectedRoute>} />
            
            {/* Add more protected routes here if needed, nested within the Layout */}
            {/* THESE ARE THE LINES YOU NEED TO UNCOMMENT: */}
            <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
            <Route path="/home" element={<ProtectedRoute><HomePage /></ProtectedRoute>} />
          </Route>

          {/* Optional: Catch-all route for unmatched paths (display a 404 page) */}
          {/* <Route path="*" element={<NotFoundPage />} /> */}
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;