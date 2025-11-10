# E-Commerce Platform Architecture

## Overview
This is a full-stack e-commerce web application built with FastAPI (Python) backend, React frontend, and MongoDB database.

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: Bcrypt via Passlib
- **CORS**: Enabled for cross-origin requests

### Frontend
- **Framework**: React 19
- **Routing**: React Router DOM v7
- **State Management**: Context API + useReducer
- **Styling**: Tailwind CSS + shadcn/ui components
- **HTTP Client**: Axios
- **Notifications**: Sonner (toast notifications)
- **Icons**: Lucide React

### Database Schema

#### Users Collection
```javascript
{
  id: String (UUID),
  email: String (unique),
  name: String,
  password_hash: String,
  created_at: DateTime (ISO string)
}
```

#### Products Collection
```javascript
{
  id: String (UUID),
  name: String,
  description: String,
  price: Float,
  category: String,
  image: String (URL),
  stock: Integer,
  created_at: DateTime (ISO string)
}
```

#### Cart Collection
```javascript
{
  id: String (UUID),
  user_id: String (references Users.id),
  product_id: String (references Products.id),
  quantity: Integer,
  created_at: DateTime (ISO string)
}
```

## Architecture Patterns

### Backend Architecture
1. **RESTful API Design**: All endpoints follow REST conventions
2. **Async/Await**: Using Motor for non-blocking database operations
3. **JWT Authentication**: Stateless authentication with Bearer tokens
4. **Model Validation**: Pydantic models for request/response validation
5. **Error Handling**: HTTP exceptions with meaningful error messages

### Frontend Architecture
1. **Context + Reducer Pattern**: 
   - `AuthContext`: Manages user authentication state
   - `CartContext`: Manages shopping cart state
2. **Component Structure**:
   - Pages: Full-page components (Home, Products, Cart, etc.)
   - Components: Reusable UI components (Navbar, ProductCard, etc.)
3. **Protected Routes**: Checkout requires authentication
4. **Local Storage**: Guest cart persisted in localStorage

## Key Features

### Authentication Flow
1. User registers/logs in
2. Backend validates credentials and returns JWT token
3. Token stored in localStorage
4. Token included in Authorization header for protected requests
5. Guest cart automatically synced after login

### Cart Management
1. **Guest Users**: Cart stored in localStorage
2. **Authenticated Users**: Cart stored in database
3. **Cart Sync**: When guest logs in, their cart merges with user cart
4. **Quantity Management**: Add, update, remove items

### Product Discovery
1. Browse all products
2. Search by name
3. Filter by category
4. View detailed product information
5. Add to cart from product list or detail page

### Checkout Process (Mock)
1. View cart summary
2. Proceed to checkout (requires login)
3. Enter payment details (mock)
4. Place order
5. Order confirmation

## API Endpoints

See `docs/api-endpoints.md` for detailed API documentation.

## Security Considerations
1. Passwords hashed with bcrypt
2. JWT tokens for stateless authentication
3. CORS configured for allowed origins
4. Input validation with Pydantic
5. Protected routes require valid JWT

## Performance Optimizations
1. Async database operations
2. MongoDB indexing on frequently queried fields
3. Component memoization where appropriate
4. Lazy loading of routes (can be added)
5. Image optimization via Unsplash CDN

## Scalability Considerations
1. Stateless backend (horizontal scaling ready)
2. MongoDB sharding support
3. JWT eliminates session storage
4. CDN for static assets
5. Load balancer ready

## Future Enhancements
1. Real payment gateway integration (Stripe)
2. Order history and tracking
3. Product reviews and ratings
4. Wishlist functionality
5. Admin dashboard for product management
6. Email notifications
7. Advanced search with filters
8. Inventory management
9. Multiple payment methods
10. Address management