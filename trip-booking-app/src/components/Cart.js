import React, { useState, useEffect } from "react";
import axios from "axios";

const Cart = () => {
  const [cart, setCart] = useState([]);

  useEffect(() => {
    const fetchCart = async () => {
      const response = await axios.get("http://localhost:8000/cart/", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      });
      setCart(response.data.items);
    };
    fetchCart();
  }, []);

  const handleDelete = async (id) => {
    await axios.delete(`http://localhost:8000/cart/`, {
      data: { id },
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
    });
    setCart(cart.filter((item) => item.id !== id));
  };

  return (
    <div>
      <h2>Your Cart</h2>
      <ul>
        {cart.map((item) => (
          <li key={item.id}>
            <p>{item.trip_name}</p>
            <p>Persons: {item.persons}</p>
            <p>Total Price: ${item.total_price}</p>
            <button onClick={() => handleDelete(item.id)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Cart;
