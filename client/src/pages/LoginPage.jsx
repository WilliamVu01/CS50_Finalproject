// client/src/pages/LoginPage.jsx
import React from 'react';
import LoginForm from '../components/Auth/LoginForm'; // Correct relative import path

function LoginPage() {
  return (
    <div className="flex justify-center items-center min-h-[calc(100vh-64px)]">
      <LoginForm />
    </div>
  );
}

export default LoginPage;
