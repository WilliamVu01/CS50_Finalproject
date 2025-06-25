// client/src/pages/CalendarPage.jsx
import React, { useState, useEffect, useCallback } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import { toast } from 'react-hot-toast';

import BookingModal from '../components/Bookings/BookingModal'; // Import BookingModal
import apiService from '../services/api'; // Import apiService to fetch real bookings
import { useAuth } from '../context/AuthContext'; // Import useAuth to get user role

function CalendarPage() {
  const { user } = useAuth(); // Get the current user from AuthContext
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedBooking, setSelectedBooking] = useState(null); // Stores data for editing
  const [selectedDateRange, setSelectedDateRange] = useState(null); // Stores data for new booking creation
  const [noBookingsMessage, setNoBookingsMessage] = useState(''); // State for specific on-page message

  // Function to fetch bookings from the backend
  const fetchBookings = useCallback(async () => {
    setLoading(true);
    setError(null);
    setNoBookingsMessage(''); // Clear previous no bookings message
    try {
      // apiService.getBookings now handles camelCase to snake_case transformation for response.
      const data = await apiService.getBookings(); 
      
      let filteredData = data;
      // Re-introducing optional client-side filtering logic for display purposes.
      // This is a temporary solution if backend filtering isn't in place yet.
      if (user) {
        if (user.role === 'student') {
          filteredData = data.filter(booking => booking.student_id === user.id);
        } else if (user.role === 'instructor') {
          filteredData = data.filter(booking => booking.instructor_id === user.id);
        }
      }

      if (filteredData.length === 0) {
        if (user?.role === 'student') { // Use optional chaining for user
          setNoBookingsMessage("No training elements booked for you. Please consult your instructor or administrator.");
        } else if (user?.role === 'instructor') { // Use optional chaining for user
          setNoBookingsMessage("You have no training elements booked. Please arrange new bookings with your students.");
        } else { // For admin or other roles
          setNoBookingsMessage("No training elements have been booked yet.");
        }
        setEvents([]); // Ensure events array is empty
      } else {
        setNoBookingsMessage(''); // Clear message if bookings are found
        // Map backend booking structure (now snake_case due to apiService transformation) to FullCalendar event structure
        const formattedEvents = filteredData.map(booking => ({
          id: booking.id,
          title: booking.training_element_name || 'No Title', // Use snake_case
          start: booking.start_time, // Use snake_case
          end: booking.end_time,     // Use snake_case
          color: '#4CAF50', // Default color, can be dynamic based on training element or status
          // Pass all original booking data (which is now snake_case) into extendedProps for easy access in modal
          extendedProps: {
            ...booking,
            // These keys already match the snake_case format from apiService, so no remapping needed here
          }
        }));
        setEvents(formattedEvents);
      }
    } catch (err) {
      setError("Failed to load bookings. Please try again.");
      console.error("Error fetching bookings:", err);
      toast.error("Failed to load bookings."); // This toast is for actual fetch errors
    } finally {
      setLoading(false);
    }
  }, [user]); // Re-run when user changes


  useEffect(() => {
    if (user) { // Only fetch bookings once user data is available
      fetchBookings();
    }
  }, [fetchBookings, user]);


  const handleEventClick = (clickInfo) => {
    // Open modal to edit existing booking
    setSelectedBooking(clickInfo.event.extendedProps); // Pass all extendedProps (original booking data)
    setIsModalOpen(true);
  };

  const handleDateSelect = (selectInfo) => {
    // Open modal to create new booking, pre-filling start/end times
    setSelectedBooking(null); // Clear any previous selection
    setSelectedDateRange({ start: selectInfo.startStr, end: selectInfo.endStr });
    setIsModalOpen(true);
  };

  const handleEventDrop = async (dropInfo) => {
    // Triggered when an event is dragged and dropped on the calendar
    const { event } = dropInfo;
    const updatedBookingData = {
      ...event.extendedProps, // Use existing extendedProps for other fields (already snake_case)
      start_time: event.startStr, // FullCalendar gives startStr in ISO format
      end_time: event.endStr,     // FullCalendar gives endStr in ISO format
    };

    try {
      await apiService.updateBooking(event.id, updatedBookingData); // CHANGED: Using apiService; transformation handled within apiService
      toast.success(`Booking "${event.title}" moved successfully!`);
      // No need to call fetchBookings directly, as FullCalendar visually updates,
      // and we expect the backend's response to confirm the change.
      // If backend failure means the change shouldn't stick, you'd revert the event.
    } catch (error) {
      toast.error(error.message || String(error)); // Ensure error is a string
      console.error("Error moving booking:", error);
      // Revert the event's position if the API call fails
      dropInfo.revert();
    }
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setSelectedBooking(null);
    setSelectedDateRange(null);
  };

  const handleBookingSuccess = () => {
    // Callback from BookingModal after successful create/update/delete
    fetchBookings(); // Re-fetch all bookings to update the calendar display
  };


  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[calc(100vh-64px)] text-xl text-gray-700">
        Loading Calendar...
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 ml-3"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-[calc(100vh-64px)] text-xl text-red-600">
        Error: {error}
      </div>
    );
  }

  return (
    <div className="p-4 md:p-8 w-full max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">Training Schedule</h1>
      <div className="bg-white p-6 rounded-lg shadow-xl">
        <FullCalendar
          plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
          headerToolbar={{
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
          }}
          initialView="dayGridMonth"
          editable={true}
          selectable={true}
          selectMirror={true}
          dayMaxEvents={true}
          weekends={true}
          events={events} // Now fetching real data
          eventClick={handleEventClick} // Opens modal for editing
          select={handleDateSelect}   // Opens modal for new booking
          eventDrop={handleEventDrop} // Handles event drag-and-drop
          height="auto"
          contentHeight="auto"
          eventContent={(arg) => {
            return (
              <div className="p-1 text-xs">
                <b>{arg.timeText}</b>
                <br />
                <i>{arg.event.title}</i>
                {arg.event.extendedProps.instructor_first_name && arg.event.extendedProps.instructor_last_name && (
                  <div className="text-gray-700">Instr: {arg.event.extendedProps.instructor_first_name} {arg.event.extendedProps.instructor_last_name}</div>
                )}
                {arg.event.extendedProps.student_first_name && arg.event.extendedProps.student_last_name && (
                  <div className="text-gray-700">Student: {arg.event.extendedProps.student_first_name} {arg.event.extendedProps.student_last_name}</div>
                )}
              </div>
            );
          }}
        />
        {noBookingsMessage && ( // Display message below calendar if there are no bookings
          <div className="text-center text-lg text-gray-600 mt-4">
            {noBookingsMessage}
            {user?.role === 'instructor' && ( // Use optional chaining for user
              <p className="mt-2 text-base">
                You can create new bookings by clicking and dragging on the calendar.
              </p>
            )}
          </div>
        )}
      </div>

      <BookingModal
        isOpen={isModalOpen}
        onClose={handleModalClose}
        initialData={selectedBooking || selectedDateRange}
        onBookingSuccess={handleBookingSuccess}
      />
    </div>
  );
}

export default CalendarPage;
