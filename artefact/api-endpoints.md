# API Endpoints Documentation

Base URL: `http://localhost:8001/api` (development)

## Authentication

### Register User
**POST** `/api/auth/register`

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-here",
    "email": "john@example.com",
    "name": "John Doe"
  }
}
```

**Error Responses:**
- `400 Bad Request`: Email already registered

---

### Login User
**POST** `/api/auth/login`

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-here",
    "email": "john@example.com",
    "name": "John Doe"
  }
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials

---

### Get Current User
**GET** `/api/auth/me`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "id": "uuid-here",
  "email": "john@example.com",
  "name": "John Doe"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or expired token

---

## Products

### Get All Products
**GET** `/api/products`

**Query Parameters:**
- `search` (optional): Search products by name
- `category` (optional): Filter by category

**Example:**
```
GET /api/products?search=headphones&category=Electronics
```

**Response:** `200 OK`
```json
[
  {
    "id": "uuid-here",
    "name": "Wireless Bluetooth Headphones",
    "description": "Premium noise-canceling headphones...",
    "price": 199.99,
    "category": "Electronics",
    "image": "https://images.unsplash.com/...",
    "stock": 50,
    "created_at": "2025-01-15T10:30:00Z"
  }
]
```

---

### Get Product by ID
**GET** `/api/products/{product_id}`

**Response:** `200 OK`
```json
{
  "id": "uuid-here",
  "name": "Wireless Bluetooth Headphones",
  "description": "Premium noise-canceling headphones...",
  "price": 199.99,
  "category": "Electronics",
  "image": "https://images.unsplash.com/...",
  "stock": 50,
  "created_at": "2025-01-15T10:30:00Z"
}
```

**Error Responses:**
- `404 Not Found`: Product not found

---

## Cart (Protected)

### Get User Cart
**GET** `/api/cart`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
[
  {
    "id": "cart-item-uuid",
    "product": {
      "id": "product-uuid",
      "name": "Wireless Bluetooth Headphones",
      "description": "Premium noise-canceling headphones...",
      "price": 199.99,
      "category": "Electronics",
      "image": "https://images.unsplash.com/...",
      "stock": 50,
      "created_at": "2025-01-15T10:30:00Z"
    },
    "quantity": 2
  }
]
```

**Error Responses:**
- `401 Unauthorized`: Invalid or expired token

---

### Add Item to Cart
**POST** `/api/cart`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "product_id": "product-uuid",
  "quantity": 2
}
```

**Response:** `200 OK`
```json
{
  "id": "cart-item-uuid",
  "product": {
    "id": "product-uuid",
    "name": "Wireless Bluetooth Headphones",
    "price": 199.99,
    "...": "..."
  },
  "quantity": 2
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or expired token
- `404 Not Found`: Product not found

---

### Update Cart Item Quantity
**PATCH** `/api/cart/{cart_id}`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "quantity": 3
}
```

**Response:** `200 OK`
```json
{
  "id": "cart-item-uuid",
  "product": { "...": "..." },
  "quantity": 3
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or expired token
- `404 Not Found`: Cart item not found

---

### Remove Item from Cart
**DELETE** `/api/cart/{cart_id}`

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "message": "Item removed from cart"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or expired token
- `404 Not Found`: Cart item not found

---

### Sync Guest Cart
**POST** `/api/cart/sync`

**Description:** Merge guest cart with user cart after login

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
[
  {
    "product_id": "product-uuid-1",
    "quantity": 2
  },
  {
    "product_id": "product-uuid-2",
    "quantity": 1
  }
]
```

**Response:** `200 OK`
```json
{
  "message": "Cart synced successfully"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or expired token

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK`: Successful request
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Authentication required or invalid token
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

**Error Response Format:**
```json
{
  "detail": "Error message here"
}
```
