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

**Endpoint:** `/login/`

**Method:** `POST`

**Description:** This endpoint allows you to login user.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "password123",
}

**Response Body:**
```json
{
    "message": "Login successful",
    "refresh": "string token",
    "access": "string token"
}

**Endpoint:** `/trip/`

**Method:** `GET`

**Description:** This endpoint allows you to view different trips available. Its landing page.

**Request Body:**
```json
{
    
}

**Response Body:**
```json
{
    [
        {
                    "id": 1,//trip id
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
}

