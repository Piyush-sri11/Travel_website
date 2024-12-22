import React from "react";
import axios from "axios";
import { useNavigate } from 'react-router-dom';


const Checkout = () => {
  const navigate = useNavigate();


  const handleCheckout = async () => {
    try {
      const response = await axios.post("http://localhost:8000/checkout/", null, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      });
      alert(response.data.message);
      navigate("/bookings");
    } catch (error) {
      alert("Checkout failed: " + error.response.data.message);
    }
  };

  return (
    <div>
      <h2>Checkout</h2>
      <button onClick={handleCheckout}>Proceed to Payment</button>
    </div>
  );
};

export default Checkout;
