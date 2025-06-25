import React, { useState, useEffect } from 'react';
import { toast } from 'react-hot-toast';
import apiService from '../../services/api'; // Correct relative import for apiService

// Basic Modal component structure 
const Modal = ({ isOpen, onClose, children }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-md mx-auto relative">
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-gray-500 hover:text-gray-700 text-2xl font-bold"
        >
          &times;
        </button>
        {children}
      </div>
    </div>
  );
};

// Main TrainingElementModal component
function TrainingElementModal({ isOpen, onClose, initialData, onSaveSuccess }) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    duration_minutes: '', 
    session_type: '', 
    material_link: '', 
  });
  const [loading, setLoading] = useState(false);

  // Update form data when initialData changes (for editing)
  useEffect(() => {
    if (initialData) {
      setFormData({
        name: initialData.name || '',
        description: initialData.description || '',
        duration_minutes: initialData.duration_minutes || '',
        session_type: initialData.session_type || '',
        material_link: initialData.material_link || '',
      });
    } else {
      // Reset form for new creation
      setFormData({
        name: '',
        description: '',
        duration_minutes: '',
        session_type: '',
        material_link: '',
      });
    }
  }, [initialData, isOpen]); 

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    if (!formData.name || !formData.duration_minutes || !formData.session_type) {
      toast.error("Name, Duration, and Session Type are required.");
      setLoading(false);
      return;
    }

    if (isNaN(formData.duration_minutes) || parseInt(formData.duration_minutes) <= 0) {
      toast.error("Duration must be a positive number.");
      setLoading(false);
      return;
    }

    try {
      let response;
      if (initialData && initialData.id) {
        response = await apiService.updateTrainingElement(initialData.id, formData);
        toast.success(response.message || 'Training element updated successfully!');
      } else {
        response = await apiService.createTrainingElement(formData);
        toast.success(response.message || 'Training element created successfully!');
      }
      onSaveSuccess(); // Refresh the list of elements after save
      onClose();     // Close the modal
    } catch (error) {
      toast.error(error.message || `Failed to save training element: ${error.toString()}`);
      console.error("Error saving training element:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <h2 className="text-2xl font-bold mb-4 text-gray-800 text-center">
        {initialData ? 'Edit Training Element' : 'Create New Training Element'}
      </h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 text-left">
            Name:
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 text-left">
            Description:
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="3"
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          ></textarea>
        </div>

        <div>
          <label htmlFor="duration_minutes" className="block text-sm font-medium text-gray-700 text-left">
            Duration (minutes):
          </label>
          <input
            type="number"
            id="duration_minutes"
            name="duration_minutes"
            value={formData.duration_minutes}
            onChange={handleChange}
            required
            min="1"
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>

        <div>
          <label htmlFor="session_type" className="block text-sm font-medium text-gray-700 text-left">
            Session Type:
          </label>
          <input
            type="text"
            id="session_type"
            name="session_type"
            value={formData.session_type}
            onChange={handleChange}
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>

        <div>
          <label htmlFor="material_link" className="block text-sm font-medium text-gray-700 text-left">
            Material Link (URL):
          </label>
          <input
            type="url"
            id="material_link"
            name="material_link"
            value={formData.material_link}
            onChange={handleChange}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>

        <div className="flex justify-end space-x-3 mt-6">
          {initialData && initialData.id && (
            <button
              type="button"
              onClick={async () => {
                toast.custom((t) => (
                  <div className={`${t.visible ? 'animate-enter' : 'animate-leave'}
                    max-w-md w-full bg-white shadow-lg rounded-lg pointer-events-auto flex ring-1 ring-black ring-opacity-5`}>
                    <div className="flex-1 w-0 p-4">
                      <div className="flex items-start">
                        <div className="flex-shrink-0 pt-0.5">
                          <svg className="h-6 w-6 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                        </div>
                        <div className="ml-3 flex-1">
                          <p className="text-sm font-medium text-gray-900">
                            Confirm Delete
                          </p>
                          <p className="mt-1 text-sm text-gray-500">
                            Are you sure you want to delete this training element?
                          </p>
                        </div>
                      </div>
                    </div>
                    <div className="flex border-l border-gray-200">
                      <button
                        onClick={async () => {
                          toast.dismiss(t.id);
                          setLoading(true);
                          try {
                            const response = await apiService.deleteTrainingElement(initialData.id); 
                            toast.success(response.message || "Training element deleted successfully!");
                            onSaveSuccess();
                            onClose();
                          } catch (error) {
                            toast.error(error.message || String(error));
                            console.error("Failed to delete training element:", error);
                          } finally {
                            setLoading(false);
                          }
                        }}
                        className="w-full border border-transparent rounded-none rounded-r-lg p-4 flex items-center justify-center text-sm font-medium text-red-600 hover:text-red-800 focus:outline-none focus:ring-2 focus:ring-red-500"
                      >
                        Delete
                      </button>
                      <button
                        onClick={() => toast.dismiss(t.id)}
                        className="w-full border border-transparent rounded-none rounded-r-lg p-4 flex items-center justify-center text-sm font-medium text-gray-700 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-500"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ), { duration: Infinity });
              }}
              className="inline-flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
              disabled={loading}
            >
              Delete
            </button>
          )}
          <button
            type="submit"
            className="inline-flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            disabled={loading}
          >
            {loading ? 'Saving...' : (initialData ? 'Update Element' : 'Create Element')}
          </button>
        </div>
      </form>
    </Modal>
  );
}

export default TrainingElementModal;