// client/src/pages/CalendarPage.jsx
import React, { useState, useEffect, useCallback, useRef } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import { toast } from 'react-hot-toast';

import BookingModal from '../components/Bookings/BookingModal'; // Import BookingModal
import apiService from '../services/api'; // Import apiService to fetch real bookings
import { useAuth } from '../context/AuthContext'; // Import useAuth to get user role

// Define a larger and more visually distinct palette of colors for events
const EVENT_COLORS_PALETTE = [
  '#4CAF50', // Green
  '#2196F3', // Blue
  '#FFC107', // Amber
  '#E91E63', // Pink
  '#9C27B0', // Purple
  '#00BCD4', // Cyan
  '#FF5722', // Deep Orange
  '#795548', // Brown
  '#673AB7', // Deep Purple
  '#CDDC39', // Lime
  '#F44336', // Red
  '#607D8B', // Blue Grey
  '#8BC34A', // Light Green
  '#03A9F4', // Light Blue
  '#FF9800', // Orange
];

// We'll use a ref to store the color mapping, so it persists across renders
// but doesn't trigger re-renders itself.
// This map will store: trainingElementId -> assignedColor
const colorMap = new Map();
let colorIndex = 0; // Tracks the next color to assign from the palette

const getUniqueColorForTrainingElement = (trainingElementId) => {
  if (typeof trainingElementId !== 'number' || trainingElementId === null) {
    console.warn("Invalid trainingElementId provided for color assignment:", trainingElementId);
    return '#A0A0A0'; // Default grey for invalid IDs
  }

  // If we've already assigned a color to this trainingElementId, return it
  if (colorMap.has(trainingElementId)) {
    return colorMap.get(trainingElementId);
  }

  // Otherwise, assign a new color from the palette
  const assignedColor = EVENT_COLORS_PALETTE[colorIndex % EVENT_COLORS_PALETTE.length];
  colorMap.set(trainingElementId, assignedColor); // Store the assignment
  colorIndex++; // Move to the next color for the next unique ID
  return assignedColor;
};

function CalendarPage() {
  // Get the current user, auth readiness, and login status from AuthContext
  const { user, isAuthReady, isLoggedIn } = useAuth();
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
    console.log("Fetching bookings for user:", user); // Debug log
    try {
      // apiService.getBookings now handles camelCase to snake_case transformation for response.
      const data = await apiService.getBookings();
      console.log("Fetched raw booking data (camelCase from apiService):", data); // Debug log

      let filteredData = data;
      // Filter bookings based on user role if logged in
      if (user) {
        if (user.role === 'student') {
          filteredData = data.filter(booking => booking.studentId === user.id); // Use camelCase studentId
        } else if (user.role === 'instructor') {
          filteredData = data.filter(booking => booking.instructorId === user.id); // Use camelCase instructorId
        }
        // Admin user sees all bookings (no additional filtering)
      }
      console.log("Filtered booking data (after user role filter):", filteredData); // Debug log


      if (filteredData.length === 0) {
        if (user?.role === 'student') { // Use optional chaining for user
          setNoBookingsMessage("No training elements booked for you. Please consult your instructor or administrator.");
        } else if (user?.role === 'instructor') { // Use optional chaining for user
          setNoBookingsMessage("You have no training elements booked. Please arrange new bookings with your students.");
        } else { // For admin or other roles, or if no user is logged in
          setNoBookingsMessage("No training elements have been booked yet.");
        }
        setEvents([]); // Ensure events array is empty
      } else {
        setNoBookingsMessage(''); // Clear message if bookings are found
        // Reset color mapping and index on fresh data fetch to re-assign colors cleanly
        colorMap.clear();
        colorIndex = 0;

        // Map backend booking structure (now camelCase from apiService) to FullCalendar event structure
        const formattedEvents = filteredData.map(booking => {
          console.log("DEBUG: Booking for color assignment:", {
            id: booking.id,
            trainingElementId: booking.trainingElementId,
            trainingElementName: booking.trainingElementName,
            // Include other relevant props if needed for more context
          });

          // Assign color based on booking.trainingElementId for consistent coloring per training element
          const color = getUniqueColorForTrainingElement(booking.trainingElementId);
          console.log(`Assigned color for trainingElementId ${booking.trainingElementId}: ${color}`); // Log the assigned color
          return {
            id: booking.id,
            title: booking.trainingElementName || 'No Title',
            start: booking.startTime,
            end: booking.endTime,
            color: color, // Use the assigned color for FullCalendar's internal use
            // Pass all original booking data (which is now camelCase) into extendedProps for easy access in modal
            extendedProps: {
              ...booking,
              assignedColor: color, // Store the assigned color in extendedProps for eventContent
            }
          };
        });
        setEvents(formattedEvents);
        console.log("Formatted events for FullCalendar:", formattedEvents); // Debug log
      }
    } catch (err) {
      setError("Failed to load bookings. Please try again.");
      console.error("Error fetching bookings:", err);
      toast.error("Failed to load bookings."); // This toast is for actual fetch errors
    } finally {
      setLoading(false);
    }
  }, [user]); // Re-run when user changes


  // This useEffect ensures fetchBookings runs once the auth state is determined
  // and a user is logged in.
  useEffect(() => {
    if (isAuthReady && isLoggedIn) {
      console.log("Auth is ready and user is logged in, initiating fetchBookings..."); // Debug log
      fetchBookings();
    } else if (isAuthReady && !isLoggedIn) {
      // If auth is ready but no user is logged in, stop loading and clear events
      setLoading(false);
      setEvents([]);
      setNoBookingsMessage("Please log in to view and manage your training schedule."); // Set a message for non-logged-in users
    }
  }, [fetchBookings, isAuthReady, isLoggedIn]);


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
      // Use extendedProps, which are already camelCase
      ...event.extendedProps,
      // FullCalendar provides startStr/endStr, which are ISO strings, compatible with backend
      startTime: event.startStr, // Use camelCase startTime for update payload
      endTime: event.endStr,     // Use camelCase endTime for update payload
    };

    try {
      await apiService.updateBooking(event.id, updatedBookingData); // apiService will convert camelCase to snake_case for backend
      toast.success(`Booking "${event.title}" moved successfully!`);
      // FullCalendar visually updates, and backend response confirms.
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

  // Conditional rendering: If not logged in, show a message instead of the calendar
  if (!isLoggedIn) {
    return (
      <div className="p-4 md:p-8 w-full max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">Training Schedule</h1>
        <div className="bg-white p-6 rounded-lg shadow-xl text-center">
          <p className="text-lg text-gray-700">Please log in to view and manage your training schedule.</p>
          <p className="mt-2 text-md text-gray-500">You can log in or register using the links in the navigation bar.</p>
        </div>
      </div>
    );
  }

  // If logged in, render the FullCalendar and booking modal
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
          events={events} // Now fetching real data (can be empty array if no bookings)
          eventClick={handleEventClick} // Opens modal for editing
          select={handleDateSelect}   // Opens modal for new booking
          eventDrop={handleEventDrop} // Handles event drag-and-drop
          height="auto"
          contentHeight="auto"
          eventContent={(arg) => {
            // Access camelCase properties from extendedProps
            const instructorName = arg.event.extendedProps.instructorFirstName && arg.event.extendedProps.instructorLastName
              ? `${arg.event.extendedProps.instructorFirstName} ${arg.event.extendedProps.instructorLastName}`
              : null;
            const studentName = arg.event.extendedProps.studentFirstName && arg.event.extendedProps.studentLastName
              ? `${arg.event.extendedProps.studentFirstName} ${arg.event.extendedProps.studentLastName}`
              : null;

            return (
              // FIXED: Apply background color directly using style prop
              <div className="p-1 text-xs" style={{ backgroundColor: arg.event.extendedProps.assignedColor || '#A0A0A0', borderRadius: '4px', overflow: 'hidden' }}>
                <b>{arg.timeText}</b>
                <br />
                <i>{arg.event.title}</i> {/* title is already set from trainingElementName */}
                {instructorName && (
                  <div className="text-gray-700">Instr: {instructorName}</div>
                )}
                {studentName && (
                  <div className="text-gray-700">Student: {studentName}</div>
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
        onSaveSuccess={handleBookingSuccess}
      />
    </div>
  );
}

export default CalendarPage;
