import React, { useState, useEffect } from "react";
import axios from "axios";

const ViewBookings = () => {
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    const fetchBookings = async () => {
      const response = await axios.get("http://localhost:8000/view-booking/", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      });
      setBookings(response.data);
    };
    fetchBookings();
  }, []);

  return (
    <div>
      <h2>Your Bookings</h2>
      <ul>
        {bookings.map((booking) => (
          <li key={booking.id}>
            <h3>{booking.trip.name}</h3>
            <p>Persons: {booking.total_persons}</p>
            <p>Total Price: ${booking.total_price}</p>
            <p>Status: {booking.status}</p>
            <button>Cancel Booking</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ViewBookings;
