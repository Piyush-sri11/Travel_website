import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav>
      <ul>
        <li><Link to="/register">Register</Link></li>
        <li><Link to="/login">Login</Link></li>
        <li><Link to="/trips">Trips</Link></li>
        <li><Link to="/cart">Cart</Link></li>
        <li><Link to="/bookings">Bookings</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;
