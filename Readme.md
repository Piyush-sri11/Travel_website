# Backend

## Project Overview

This project is a travel itinerary platform that offers curated travel experiences designed by influencers. The backend is built using Django and Django REST framework.

## Features

- API endpoints for user registration, login, trip viewing, cart management, and checkout.
- Integration with a database to store and retrieve travel data.
- Authentication and authorization for user accounts.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Piyush-sri11/Travel_website.git
   ```
2. Set up a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

# Running the Server

1. Navigate to the backend directory:
   ```bash
   cd travel
   ```
2. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
3. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Testing

1. Run tests using `pytest`:
   ```bash
   pytest
   ```

# Frontend

## Project Overview

This project is a travel itinerary platform that offers curated travel experiences designed by influencers. The frontend is built using React and Tailwind CSS.

## Features

- Navigation bar with links to Home, Dashboard, Cart, Login, and Register.
- Header section with a background image and search input.
- Display of upcoming popular explorations with details such as title, tags, info, price, curator, and available spots.
- Responsive design with Tailwind CSS.

## Running

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

## Usage

- Ensure backend is running
- Navigate to `http://localhost:3000` to view the application.


## API Documentation

### Register a New User

**Endpoint:** `/register/`

**Method:** `POST`

**Description:** This endpoint allows you to register a new user.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe"
}
```

**Response Body:**
```json
{
    "message": "User registered successfully",
    "user_id": 1
}
```

### Login User

**Endpoint:** `/login/`

**Method:** `POST`

**Description:** This endpoint allows you to login user.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```

**Response Body:**
```json
{
    "message": "Login successful",
    "refresh": "string token",
    "access": "string token"
}
```

### View Trips

**Endpoint:** `/trip/`

**Method:** `GET`

**Description:** This endpoint allows you to view different trips available. Its landing page.

**Request Body:**
```json
{
    
}
```

**Response Body:**
```json
[
    {
        "id": 1, //trip id
        "organizer": {
            "id": 2, //user id
            "first_name": "Johny",
            "last_name": "Walker"
        },
        "name": "Kasol", //trip name
        "description": "Brownie",
        "start_date": "2025-01-01",
        "end_date": "2025-01-10",
        "price": "3999.99",
        "total_slots": 12,
        "available_slots": 6,
        "cancellation_policy": ""
    },
    {
        "id": 3,
        "organizer": {
            "id": 2,
            "first_name": "Johny",
            "last_name": "Walker"
        },
        "name": "Jaipur",
        "description": "Padharo mhare desh",
        "start_date": "2025-02-10",
        "end_date": "2025-02-15",
        "price": "2999.99",
        "total_slots": 12,
        "available_slots": 12,
        "cancellation_policy": ""
    }
]
```


### Logout User

**Endpoint:** `/logout/`

**Method:** `POST`

**Description:** This endpoint allows you to logout user.

**Request Body:**
```json
{
    "refresh": "string token"
}
```

**Response Body:**
```json
{
    "message": "Logout successful"
}
```

### View Cart

**Endpoint:** `/cart/`

**Method:** `GET`

**Description:** This endpoint allows you to view the items in the cart.

**Request Headers:**
```json
{
    "Authorization": "Bearer token",
    "Content-Type": "application/json"
}
```

**Request Body:**
```json
{
    
}
```

**Response Body:**
```json
[
    {
        "trip_id": 1,
        "name": "Kasol",
        "price": "3999.99",
        "quantity": 2
    },
    {
        "trip_id": 3,
        "name": "Jaipur",
        "price": "2999.99",
        "quantity": 1
    }
]
```

### Add to Cart

**Endpoint:** `/cart/`

**Method:** `POST`

**Description:** This endpoint allows you to add a trip to the cart.

**Request Headers:**
```json
{
    "Authorization": "Bearer token",
    "Content-Type": "application/json"
}
```

**Request Body:**
```json
{
    "id": 1, // trip id required
    "persons": 5 // no persons
}
```

**Response Body:**
```json
{
    "message": "Trip added to cart successfully",
    "cart_item_id": 1
}
```

### Remove from Cart

**Endpoint:** `/cart/`

**Method:** `DELETE`

**Description:** This endpoint allows you to remove a trip from the cart.

**Request Headers:**
```json
{
    "Authorization": "Bearer token",
    "Content-Type": "application/json"
}
```
**Request Body:**
```json
{
    "id": 1 //cart item id
}
```

**Response Body:**
```json
{
    "message": "Trip removed from cart successfully"
}
```

### Update Cart

**Endpoint:** `/cart/`

**Method:** `PATCH`

**Description:** This endpoint allows you to update the quantity of a trip in the cart.

**Request Headers:**
```json
{
    "Authorization": "Bearer token",
    "Content-Type": "application/json"
}
```

**Request Body:**
```json
{
    "id": 1, //cart item id
    "persons": 3
}
```

**Response Body:**
```json
{
    "message": "Cart item updated successfully"
}
```

**Checkout**

**Endpoint:** `/checkout/`

**Method:** `POST`

**Description:** `This endpoint allows you to proceed to payment and book the trips in the cart.`

**Request headers:**
```json
{
    "Authorization": "Bearer token",
    "Content-Type": "application/json"
}
```
**Response body:**
```json
{
    "message": "Booking successful"
}
```
**Cancel Booking**

**Endpoint:** `/cancel-booking/`

**Method:** `POST`

**Description:** `This endpoint allows you to cancel a booking.`

**Request headers:**
```json
{
    "Authorization": "Bearer token",
    "Content-Type": "application/json"
}
```
**Request Body:**
```json
{
    "booking_id": 1
}
```

**Response body:**
```json
{
    "message": "Booking cancelled successfully"
}
```

**View Bookings**

**Endpoint:** `/view-booking/`

**Method:** `GET`

**Description:** `This endpoint allows you to view your bookings.`

**Request headers:**
```json
{
    "Authorization": "Bearer token",
    "Content-Type": "application/json"
}
```
**Request Body:**
```json
{
  
}
```

**Response body:**
```json
{
    [
    {
        "id": 1, //booking id
        "trip": {
            "id": 1, //trip id
            "name": "Kasol",
            "description": "Brownie",
            "start_date": "2025-01-01",
            "end_date": "2025-01-10",
            "price": "3999.99",
            "total_slots": 12,
            "available_slots": 6,
            "cancellation_policy": ""
        },
        "user": 6, //user id
        "booking_date": "2024-12-20T21:11:00Z",
        "total_persons": 2,
        "total_price": "7999.98",
        "status": "CONFIRMED",
        "refund_amount": null
    }
]
}
```

### Check Organizer Existence

**Endpoint:** `/exist-org/`

**Method:** `GET`

**Description:** This endpoint allows you to check if an organizer exists.

**Request Headers:**
```json
{
    "Authorization": "Bearer token",
    "Content-Type": "application/json"
}
```
**Response Body:**
```json
{
    "message": "You are now registered as an organizer"
}
```

**Register as Organizer**

**Endpoint:** `/organizer/register/`

**Method:** `POST`

**Description:** ` This endpoint allows you to register as an organizer.`


**Request Body:**
```json
{
  "email": "organizer@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "is_organizer": true
}
```

**Response body:**
```json
{
    "user_id": 6
}
```

**Add Trip (Organizer Only)**

**Endpoint:** `/org-trips/`

**Method:** `POST`

**Description:** `This endpoint allows organizers to add new trips.`

**Request headers:**
```json
{
    "Authorization": "Bearer token",
    "Content-Type": "application/json"
}
```
**Request Body:**
```json
{
    "name": "Trip Name",
    "description": "Trip Description",
    "start_date": "2025-01-01",
    "end_date": "2025-01-10",
    "price": "3999.99",
    "total_slots": 12,
    "available_slots": 12,
    "cancellation_policy": "Cancellation Policy"
}
```

**Response body:**
```json
{
    "trip_id": 1
}
```

**View Organizer Trips (Organizer Only)**

**Endpoint:** `/org-trips/`

**Method:** `GET`

**Description:** `This endpoint allows organizers to view their trips.`

**Request headers:**
```json
{
    "Authorization": "Bearer token",
    "Content-Type": "application/json"
}
```


**Response body:**
```json
{
    [
    {
        "id": 1, //trip id
        "name": "Trip Name",
        "description": "Trip Description",
        "start_date": "2025-01-01",
        "end_date": "2025-01-10",
        "price": "3999.99",
        "total_slots": 12,
        "available_slots": 12,
        "cancellation_policy": "Cancellation Policy"
    }
]
}
```


**Delete Trip (Organizer Only)**

**Endpoint:** `/org-trips/`

**Method:** `DELETE`

**Description:** ` This endpoint allows organizers to delete a trip.`

**Request headers:**
```json
{
    "Authorization": "Bearer token",
    "Content-Type": "application/json"
}
```
**Request Body:**
```json
{
    "id": 1 //trip id
}
```

**Response body:**
```json
{
    "message": "Trip deleted successfully"
}
```

**Update Trip (Organizer Only)**

**Endpoint:** `/org-trips/`

**Method:** `PATCH`

**Description:** ` This endpoint allows organizers to update a trip.`

**Request headers:**
```json
{
    "Authorization": "Bearer token",
    "Content-Type": "application/json"
}
```
**Request Body:**
```json
{
    {
    "id": 1, //trip id required
    "name": "Updated Trip Name",
    "description": "Updated Trip Description",
    "start_date": "2025-01-01",
    "end_date": "2025-01-10",
    "price": "3999.99",
    "total_slots": 12,
    "available_slots": 12,
    "cancellation_policy": "Updated Cancellation Policy"
}
}
```

**Response body:**
```json
{
    "trip_id": 1
}
```


