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
