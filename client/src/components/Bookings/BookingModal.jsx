// client/src/components/Bookings/BookingModal.jsx
import React, { useState, useEffect } from 'react';
import { toast } from 'react-hot-toast';
import apiService from '../../services/api';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css'; // Make sure to import the CSS for react-datepicker

// Basic Modal component structure (re-used for consistency)
const Modal = ({ isOpen, onClose, children }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center z-50 overflow-y-auto p-4">
      <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-lg mx-auto relative my-8">
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

function BookingModal({ isOpen, onClose, initialData, onSaveSuccess }) {
  const [formData, setFormData] = useState({
    training_element_id: '',
    instructor_id: '',
    student_id: '',
    start_time: null,
    end_time: null,
    notes: '',
  });
  const [trainingElements, setTrainingElements] = useState([]);
  const [users, setUsers] = useState([]); // Will fetch all users and filter by role
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [selectedTrainingElementSessionType, setSelectedTrainingElementSessionType] = useState(''); // State for session type display

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const elements = await apiService.getTrainingElements();
        const fetchedUsers = await apiService.getUsers(); // Fetch all users
        setTrainingElements(elements);
        setUsers(fetchedUsers);

        if (initialData) {
          // Parse string dates to Date objects for DatePicker
          setFormData({
            training_element_id: initialData.training_element_id || '',
            instructor_id: initialData.instructor_id || '',
            student_id: initialData.student_id || '',
            start_time: initialData.start_time ? new Date(initialData.start_time) : null,
            end_time: initialData.end_time ? new Date(initialData.end_time) : null,
            notes: initialData.notes || '',
          });

          // Ensure session type is set for initial data
          const initialElement = elements.find(el => el.id === (initialData.training_element_id || initialData.trainingElementId));
          // Use initialData.training_element_id first, fallback to trainingElementId from CalendarPage's extendedProps
          if (initialElement) {
            setSelectedTrainingElementSessionType(initialElement.sessionType);
          } else {
            setSelectedTrainingElementSessionType(''); // Clear if no element found
          }
        } else {
          // Reset form for new booking
          setFormData({
            training_element_id: '',
            instructor_id: '',
            student_id: '',
            start_time: null,
            end_time: null,
            notes: '',
          });
          setSelectedTrainingElementSessionType(''); // Clear for new booking
        }
      } catch (error) {
        toast.error(error.message || 'Failed to load data for booking form.');
        console.error("Error fetching form data:", error);
      } finally {
        setLoading(false);
      }
    };

    if (isOpen) {
      fetchData();
    }
  }, [isOpen, initialData]); // initialData is a dependency because we need to re-run if it changes (e.g., from creating to editing)

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    // Update session type display when training element is selected
    if (name === 'training_element_id') {
      const selectedElement = trainingElements.find(element => element.id === parseInt(value));
      setSelectedTrainingElementSessionType(selectedElement ? selectedElement.sessionType : '');
    }
  };

  const handleDateChange = (date, name) => {
    setFormData((prev) => ({ ...prev, [name]: date }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);

    if (!formData.training_element_id || !formData.start_time || !formData.end_time || !formData.instructor_id || !formData.student_id) {
      toast.error("Please fill all required fields: Training Element, Start Time, End Time, Instructor, and Student.");
      setSaving(false);
      return;
    }

    if (formData.start_time >= formData.end_time) {
      toast.error("End time must be after start time.");
      setSaving(false);
      return;
    }

    // Prepare data for backend (send dates in ISO format)
    const dataToSend = {
      ...formData,
      start_time: formData.start_time ? formData.start_time.toISOString() : null,
      end_time: formData.end_time ? formData.end_time.toISOString() : null,
      // Ensure IDs are integers if they are strings from <select>
      training_element_id: parseInt(formData.training_element_id),
      instructor_id: parseInt(formData.instructor_id),
      student_id: parseInt(formData.student_id),
    };

    try {
      let response;
      if (initialData && initialData.id) {
        response = await apiService.updateBooking(initialData.id, dataToSend);
        toast.success(response.message || 'Booking updated successfully!');
      } else {
        response = await apiService.createBooking(dataToSend);
        toast.success(response.message || 'Booking created successfully!');
      }
      onSaveSuccess(); // Callback to refresh calendar
      onClose();
    } catch (error) {
      toast.error(error.message || `Failed to save booking: ${error.toString()}`);
      console.error("Error saving booking:", error);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!initialData || !initialData.id) return;

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
                Are you sure you want to delete this booking?
              </p>
            </div>
          </div>
        </div>
        <div className="flex border-l border-gray-200">
          <button
            onClick={async () => {
              toast.dismiss(t.id);
              setSaving(true);
              try {
                const response = await apiService.deleteBooking(initialData.id);
                toast.success(response.message || "Booking deleted successfully!");
                onSaveSuccess();
                onClose();
              } catch (error) {
                toast.error(error.message || String(error));
                console.error("Failed to delete booking:", error);
              } finally {
                setSaving(false);
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
  };


  if (loading) {
    return (
      <Modal isOpen={isOpen} onClose={onClose}>
        <div className="text-center py-8">Loading form data...</div>
      </Modal>
    );
  }

  const instructors = users.filter(user => user.role === 'instructor' || user.role === 'admin');
  const students = users.filter(user => user.role === 'student' || user.role === 'admin'); // Admin can be a student too

  // Function to format session type for display
  const formatSessionType = (type) => {
    if (!type) return '';
    return type.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <h2 className="text-2xl font-bold mb-4 text-gray-800 text-center">
        {initialData ? 'Edit Booking' : 'Create New Booking'}
      </h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="training_element_id" className="block text-sm font-medium text-gray-700 text-left">
            Training Element:
          </label>
          <select
            id="training_element_id"
            name="training_element_id"
            value={formData.training_element_id}
            onChange={handleChange}
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            <option value="">Select Training Element</option>
            {trainingElements.map((element) => (
              <option key={element.id} value={element.id}>
                {element.name} ({element.durationMinutes} min)
              </option>
            ))}
          </select>
        </div>

        {/* FIXED: Removed conditional rendering, Session Type is now always visible */}
        <div>
          <label htmlFor="session_type_display" className="block text-sm font-medium text-gray-700 text-left">
            Session Type:
          </label>
          <input
            type="text"
            id="session_type_display"
            // Display 'N/A' or an empty string if no session type is selected/found
            value={selectedTrainingElementSessionType ? formatSessionType(selectedTrainingElementSessionType) : 'N/A'}
            readOnly
            className="mt-1 block w-full px-3 py-2 bg-gray-100 border border-gray-300 rounded-md shadow-sm sm:text-sm"
          />
        </div>

        <div>
          <label htmlFor="instructor_id" className="block text-sm font-medium text-gray-700 text-left">
            Instructor:
          </label>
          <select
            id="instructor_id"
            name="instructor_id"
            value={formData.instructor_id}
            onChange={handleChange}
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            <option value="">Select Instructor</option>
            {instructors.map((user) => (
              <option key={user.id} value={user.id}>
                {user.firstName} {user.lastName}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="student_id" className="block text-sm font-medium text-gray-700 text-left">
            Student:
          </label>
          <select
            id="student_id"
            name="student_id"
            value={formData.student_id}
            onChange={handleChange}
            required
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            <option value="">Select Student</option>
            {students.map((user) => (
              <option key={user.id} value={user.id}>
                {user.firstName} {user.lastName}
              </option>
            ))}
          </select>
        </div>

        <div className="flex space-x-4">
          <div className="flex-1">
            <label htmlFor="start_time" className="block text-sm font-medium text-gray-700 text-left">
              Start Time:
            </label>
            <DatePicker
              selected={formData.start_time}
              onChange={(date) => handleDateChange(date, 'start_time')}
              showTimeSelect
              dateFormat="Pp"
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              required
            />
          </div>
          <div className="flex-1">
            <label htmlFor="end_time" className="block text-sm font-medium text-gray-700 text-left">
              End Time:
            </label>
            <DatePicker
              selected={formData.end_time}
              onChange={(date) => handleDateChange(date, 'end_time')}
              showTimeSelect
              dateFormat="Pp"
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              required
            />
          </div>
        </div>

        <div>
          <label htmlFor="notes" className="block text-sm font-medium text-gray-700 text-left">
            Notes:
          </label>
          <textarea
            id="notes"
            name="notes"
            value={formData.notes}
            onChange={handleChange}
            rows="3"
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          ></textarea>
        </div>

        <div className="flex justify-end space-x-3 mt-6">
          {initialData && initialData.id && (
            <button
              type="button"
              onClick={handleDelete}
              className="inline-flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
              disabled={saving}
            >
              Delete
            </button>
          )}
          <button
            type="submit"
            className="inline-flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            disabled={saving}
          >
            {saving ? 'Saving...' : (initialData ? 'Update Booking' : 'Create Booking')}
          </button>
        </div>
      </form>
    </Modal>
  );
}

export default BookingModal;
