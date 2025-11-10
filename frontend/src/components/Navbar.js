import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useCart } from '../contexts/CartContext';
import { ShoppingCart, User, LogOut, Menu, X, Search } from 'lucide-react';

export const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const { getCartCount } = useCart();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const cartCount = getCartCount();

  return (
    <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg"></div>
            <span className="text-xl font-bold text-gray-900">ShopHub</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link
              to="/"
              data-testid="nav-home-link"
              className="text-gray-700 hover:text-blue-600 transition-colors font-medium"
            >
              Home
            </Link>
            <Link
              to="/products"
              data-testid="nav-products-link"
              className="text-gray-700 hover:text-blue-600 transition-colors font-medium"
            >
              Products
            </Link>
            <Link
              to="/about"
              data-testid="nav-about-link"
              className="text-gray-700 hover:text-blue-600 transition-colors font-medium"
            >
              About
            </Link>
          </div>

          {/* Right Side Actions */}
          <div className="hidden md:flex items-center space-x-4">
            <Link
              to="/cart"
              data-testid="nav-cart-link"
              className="relative p-2 text-gray-700 hover:text-blue-600 transition-colors"
            >
              <ShoppingCart className="w-6 h-6" />
              {cartCount > 0 && (
                <span
                  data-testid="cart-count-badge"
                  className="absolute -top-1 -right-1 bg-blue-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold"
                >
                  {cartCount}
                </span>
              )}
            </Link>

            {isAuthenticated ? (
              <div className="flex items-center space-x-3">
                <span data-testid="user-name" className="text-sm text-gray-700">
                  {user?.name}
                </span>
                <button
                  onClick={handleLogout}
                  data-testid="logout-button"
                  className="flex items-center space-x-1 px-4 py-2 text-gray-700 hover:text-red-600 transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Logout</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Link
                  to="/login"
                  data-testid="nav-login-link"
                  className="px-4 py-2 text-gray-700 hover:text-blue-600 transition-colors font-medium"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  data-testid="nav-register-link"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 text-gray-700"
            data-testid="mobile-menu-button"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-200" data-testid="mobile-menu">
            <div className="flex flex-col space-y-3">
              <Link
                to="/"
                data-testid="mobile-nav-home-link"
                onClick={() => setMobileMenuOpen(false)}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors block"
              >
                Home
              </Link>
              <Link
                to="/products"
                data-testid="mobile-nav-products-link"
                onClick={() => setMobileMenuOpen(false)}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors block"
              >
                Products
              </Link>
              <Link
                to="/about"
                data-testid="mobile-nav-about-link"
                onClick={() => setMobileMenuOpen(false)}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors block"
              >
                About
              </Link>
              <Link
                to="/cart"
                data-testid="mobile-nav-cart-link"
                onClick={() => setMobileMenuOpen(false)}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors flex items-center justify-between"
              >
                <span>Cart</span>
                {cartCount > 0 && (
                  <span className="bg-blue-600 text-white text-xs rounded-full px-2 py-1 font-bold">
                    {cartCount}
                  </span>
                )}
              </Link>
              {isAuthenticated ? (
                <>
                  <div className="px-4 py-2 text-sm text-gray-500">Hello, {user?.name}</div>
                  <button
                    data-testid="mobile-logout-button"
                    onClick={() => {
                      handleLogout();
                      setMobileMenuOpen(false);
                    }}
                    className="px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors text-left block w-full"
                  >
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link
                    to="/login"
                    data-testid="mobile-nav-login-link"
                    onClick={() => setMobileMenuOpen(false)}
                    className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors block"
                  >
                    Login
                  </Link>
                  <Link
                    to="/register"
                    data-testid="mobile-nav-register-link"
                    onClick={() => setMobileMenuOpen(false)}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-center block"
                  >
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};