import React, { useState, useEffect, useCallback } from 'react';
import { toast } from 'react-hot-toast';
import apiService from '../services/api';
import TrainingElementModal from '../components/TrainingElements/TrainingElementModal'; // Correct import path
import { useAuth } from '../context/AuthContext';

function TrainingElementManagement() {
  const { user } = useAuth();
  const [trainingElements, setTrainingElements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentElement, setCurrentElement] = useState(null);

  const fetchTrainingElements = useCallback(async () => {
    setLoading(true);
    try {
      const data = await apiService.getTrainingElements();
      setTrainingElements(data);
      console.log("Fetched training elements for table:", data); // Debug log
    } catch (error) {
      toast.error(error.message || 'Failed to fetch training elements.');
      console.error("Error fetching training elements:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTrainingElements();
  }, [fetchTrainingElements]);

  const handleCreateNew = () => {
    setCurrentElement(null);
    setIsModalOpen(true);
  };

  const handleEdit = (element) => {
    setCurrentElement(element);
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setCurrentElement(null);
  };

  const handleSaveSuccess = () => {
    fetchTrainingElements(); // Re-fetch elements to update the table
  };

  // Role-based access control for this page
  // Ensure user is loaded before checking role
  if (!user && loading) { // If user is null and still loading, show loading indicator for this component
    return (
      <div className="flex justify-center items-center min-h-[calc(100vh-64px)] text-xl text-gray-700">
        Loading user data for access check...
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 ml-3"></div>
      </div>
    );
  }

  // Once loading is false, if user is still null or unauthorized role, show access denied
  if (!user || (user.role !== 'admin' && user.role !== 'instructor')) {
    return (
      <div className="container mx-auto p-6 text-center text-red-500">
        <h1 className="text-3xl font-bold mb-6">Access Denied</h1>
        <p>You do not have permission to view this page. Only administrators and instructors can manage training elements.</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 bg-white shadow-md rounded-lg mt-8">
      <h1 className="text-3xl font-bold mb-6 text-gray-800 text-center">
        Training Element Management
      </h1>

      <div className="flex justify-end mb-4">
        <button
          onClick={handleCreateNew}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md shadow-md transition duration-300"
        >
          Add New Training Element
        </button>
      </div>

      {loading ? (
        <div className="text-center py-8">Loading training elements...</div>
      ) : trainingElements.length === 0 ? (
        <div className="text-center py-8 text-gray-600">No training elements found.</div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border border-gray-200 rounded-lg">
            <thead className="bg-gray-100">
              <tr>
                <th className="py-3 px-6 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Name</th>
                <th className="py-3 px-6 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Description</th> {/* Added Description column header */}
                <th className="py-3 px-6 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Duration (min)</th>
                <th className="py-3 px-6 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Session Type</th>
                <th className="py-3 px-6 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Material Link</th> {/* Added Material Link column header */}
                <th className="py-3 px-6 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {trainingElements.map((element) => (
                <tr key={element.id} className="hover:bg-gray-50">
                  <td className="py-3 px-6 whitespace-nowrap text-sm font-medium text-gray-900">{element.name}</td>
                  <td className="py-3 px-6 text-sm text-gray-700 max-w-xs truncate">{element.description}</td> {/* Display Description */}
                  {/* MINIMUM CHANGE: Changed element.duration_minutes to element.durationMinutes */}
                  <td className="py-3 px-6 whitespace-nowrap text-sm text-gray-700">{element.durationMinutes}</td>
                  {/* MINIMUM CHANGE: Changed element.session_type to element.sessionType and added formatting */}
                  <td className="py-3 px-6 whitespace-nowrap text-sm text-gray-700">
                    {element.sessionType ? element.sessionType.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase()) : 'N/A'}
                  </td>
                  <td className="py-3 px-6 whitespace-nowrap text-sm text-gray-700">
                    {element.materialLink ? (
                      <a href={element.materialLink} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-900">
                        View Link
                      </a>
                    ) : 'N/A'}
                  </td>
                  <td className="py-3 px-6 whitespace-nowrap text-sm">
                    <button
                      onClick={() => handleEdit(element)}
                      className="text-blue-600 hover:text-blue-900 font-semibold transition duration-150 ease-in-out"
                    >
                      Edit
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* CORRECTED: This component name was mismatched before. */}
      <TrainingElementModal
        isOpen={isModalOpen}
        onClose={handleModalClose}
        initialData={currentElement}
        onSaveSuccess={handleSaveSuccess}
      />
    </div>
  );
}

export default TrainingElementManagement;
