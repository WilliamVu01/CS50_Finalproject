// client/src/pages/RegisterPage.jsx
import React from 'react';
import RegisterForm from '../components/Auth/RegisterForm'; // Correct relative import path

function RegisterPage() {
  return (
    <div className="flex justify-center items-center min-h-[calc(100vh-64px)]">
      <RegisterForm />
    </div>
  );
}

export default RegisterPage;
