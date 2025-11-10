# ShopHub - E-Commerce Platform

A modern, full-stack e-commerce web application built with FastAPI, React, and MongoDB.

## Features

- **User Authentication**: Register, login, and logout with JWT
- **Product Catalog**: Browse, search, and filter products
- **Shopping Cart**: Add, update, remove items with quantity management
- **Guest Cart**: Cart persists for guests and syncs after login
- **Checkout Flow**: Mock payment processing and order confirmation
- **Responsive Design**: Mobile-first, works on all devices
- **Toast Notifications**: User feedback for all actions

## Tech Stack

### Backend
- FastAPI (Python)
- MongoDB with Motor (async driver)
- JWT authentication with bcrypt
- Pydantic for validation

### Frontend
- React 19
- React Router DOM v7
- Tailwind CSS + shadcn/ui
- Context API for state management
- Axios for HTTP requests
- Sonner for notifications

## Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB (local or Atlas)
- yarn package manager

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd app
```

### 2. Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and set your MONGO_URL and JWT_SECRET_KEY

# Seed the database with sample products
python seed_products.py

# Start the backend server
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
yarn install

# Configure environment variables
cp .env.example .env
# Edit .env and set REACT_APP_BACKEND_URL

# Start the development server
yarn start
```

## Environment Variables

### Backend (.env)
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=ecommerce_db
CORS_ORIGINS=*
JWT_SECRET_KEY=your-secret-key-change-in-production
```

### Frontend (.env)
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

## Running the Application

1. Start MongoDB (if running locally)
2. Start the backend server (port 8001)
3. Start the frontend development server (port 3000)
4. Open http://localhost:3000 in your browser

## Seeding the Database

The application includes a seed script to populate the database with sample products:

```bash
cd backend
python seed_products.py
```

This creates 12 sample products across 4 categories:
- Electronics
- Fashion
- Sports
- Home

## API Documentation

Detailed API documentation is available in `docs/api-endpoints.md`.

Base URL: `http://localhost:8001/api`

### Key Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `GET /api/products` - Get all products
- `GET /api/products/:id` - Get product by ID
- `GET /api/cart` - Get user cart (protected)
- `POST /api/cart` - Add item to cart (protected)
- `PATCH /api/cart/:id` - Update cart item (protected)
- `DELETE /api/cart/:id` - Remove cart item (protected)

## Project Structure

```
app/
├── backend/
│   ├── server.py           # FastAPI application
│   ├── seed_products.py    # Database seeding script
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
├── frontend/
│   ├── src/
│   │   ├── contexts/      # React contexts (Auth, Cart)
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── App.js         # Main app component
│   │   └── index.js       # Entry point
│   ├── package.json       # Node dependencies
│   └── .env              # Environment variables
├── docs/
│   ├── architecture.md    # System architecture
│   ├── api-endpoints.md   # API documentation
│   └── prompts-used.txt   # Development notes
└── README.md             # This file
```

## Key Features Explained

### Authentication
- JWT-based authentication
- Passwords hashed with bcrypt
- Token stored in localStorage
- Auto-login on page refresh

### Cart Management
- **Guest Users**: Cart stored in localStorage
- **Logged-in Users**: Cart stored in MongoDB
- **Cart Sync**: Guest cart automatically merges with user cart on login
- **Quantity Updates**: Increase/decrease items
- **Real-time Total**: Calculates subtotal, shipping, tax, and total

### Product Features
- Search by product name
- Filter by category
- Product detail pages
- Stock availability
- Add to cart from list or detail page

### Checkout
- Order summary with itemized list
- Shipping calculation (free over $50)
- Tax calculation (8%)
- Mock payment form
- Order confirmation

## Testing

All interactive elements include `data-testid` attributes for automated testing.

```bash
# Frontend tests (if implemented)
cd frontend
yarn test
```

## Deployment

### Backend Deployment
1. Set production environment variables
2. Use a production WSGI server (e.g., Gunicorn)
3. Configure CORS for your domain
4. Use MongoDB Atlas for production database

### Frontend Deployment
1. Build the production bundle: `yarn build`
2. Deploy to hosting service (Vercel, Netlify, etc.)
3. Set production environment variables
4. Update CORS settings on backend

## Security Considerations

- Change `JWT_SECRET_KEY` to a strong random string in production
- Use HTTPS in production
- Configure CORS to allow only your domain
- Implement rate limiting for API endpoints
- Add input sanitization for user-generated content
- Implement CSRF protection for state-changing operations

## Future Enhancements

- [ ] Real payment integration (Stripe)
- [ ] Order history and tracking
- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Admin dashboard for product management
- [ ] Email notifications
- [ ] Password reset functionality
- [ ] Social authentication (Google, Facebook)
- [ ] Advanced search with price filters
- [ ] Product recommendations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - feel free to use this project for learning or commercial purposes.

## Support

For issues or questions, please open an issue on GitHub.

## Acknowledgments

- Product images from Unsplash
- Icons from Lucide React
- UI components from shadcn/ui
- Design inspiration from modern e-commerce platforms