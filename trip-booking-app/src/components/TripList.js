import React, { useState, useEffect } from "react";
import axios from "axios";

const TripList = () => {
  const [trips, setTrips] = useState([]);

  useEffect(() => {
    const fetchTrips = async () => {
      const response = await axios.get("http://localhost:8000/trip/");
      setTrips(response.data);
    };
    fetchTrips();
  }, []);

  return (
    <div>
      <h2>Upcoming Trips</h2>
      <ul>
        {trips.map((trip) => (
          <li key={trip.id}>
            <h3>{trip.name}</h3>
            <p>{trip.description}</p>
            <p>Price: ${trip.price}</p>
            <button>Add to Cart</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TripList;
