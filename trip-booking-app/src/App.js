import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
import TripList from './components/TripList';
import Cart from './components/Cart';
import Checkout from './components/Checkout';
import ViewBookings from './components/ViewBookings';
import Navbar from './components/Navbar';

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/trips" element={<TripList />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/checkout" element={<Checkout />} />
        <Route path="/bookings" element={<ViewBookings />} />
      </Routes>
    </Router>
  );
};

export default App;