import React, { createContext, useContext, useReducer, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';

const CartContext = createContext();

const cartReducer = (state, action) => {
  switch (action.type) {
    case 'SET_CART':
      return { ...state, items: action.payload };
    case 'ADD_ITEM':
      const existingIndex = state.items.findIndex(
        (item) => item.product.id === action.payload.product.id
      );
      if (existingIndex >= 0) {
        const newItems = [...state.items];
        newItems[existingIndex].quantity += action.payload.quantity;
        return { ...state, items: newItems };
      }
      return { ...state, items: [...state.items, action.payload] };
    case 'UPDATE_ITEM':
      return {
        ...state,
        items: state.items.map((item) =>
          item.id === action.payload.id
            ? { ...item, quantity: action.payload.quantity }
            : item
        ),
      };
    case 'REMOVE_ITEM':
      return {
        ...state,
        items: state.items.filter((item) => item.id !== action.payload),
      };
    case 'CLEAR_CART':
      return { ...state, items: [] };
    default:
      return state;
  }
};

const initialState = {
  items: [],
};

export const CartProvider = ({ children }) => {
  const [state, dispatch] = useReducer(cartReducer, initialState);
  const { isAuthenticated, token } = useAuth();

  // Load cart from localStorage for guests
  useEffect(() => {
    if (!isAuthenticated) {
      const guestCart = localStorage.getItem('guestCart');
      if (guestCart) {
        dispatch({ type: 'SET_CART', payload: JSON.parse(guestCart) });
      }
    }
  }, [isAuthenticated]);

  // Fetch cart from server when authenticated
  useEffect(() => {
    if (isAuthenticated && token) {
      fetchCart();
    }
  }, [isAuthenticated, token]);

  // Save guest cart to localStorage
  useEffect(() => {
    if (!isAuthenticated) {
      localStorage.setItem('guestCart', JSON.stringify(state.items));
    }
  }, [state.items, isAuthenticated]);

  const fetchCart = async () => {
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_BACKEND_URL}/api/cart`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      dispatch({ type: 'SET_CART', payload: response.data });
    } catch (error) {
      console.error('Failed to fetch cart:', error);
    }
  };

  const syncGuestCart = async () => {
    const guestCart = localStorage.getItem('guestCart');
    if (guestCart && token) {
      try {
        const items = JSON.parse(guestCart);
        const syncData = items.map((item) => ({
          product_id: item.product.id,
          quantity: item.quantity,
        }));
        
        await axios.post(
          `${process.env.REACT_APP_BACKEND_URL}/api/cart/sync`,
          syncData,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        
        localStorage.removeItem('guestCart');
        await fetchCart();
      } catch (error) {
        console.error('Failed to sync cart:', error);
      }
    }
  };

  const addToCart = async (product, quantity = 1) => {
    if (isAuthenticated && token) {
      try {
        const response = await axios.post(
          `${process.env.REACT_APP_BACKEND_URL}/api/cart`,
          { product_id: product.id, quantity },
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        dispatch({ type: 'ADD_ITEM', payload: response.data });
      } catch (error) {
        console.error('Failed to add to cart:', error);
      }
    } else {
      // Guest cart
      const newItem = {
        id: `guest-${Date.now()}`,
        product,
        quantity,
      };
      dispatch({ type: 'ADD_ITEM', payload: newItem });
    }
  };

  const updateQuantity = async (itemId, quantity) => {
    if (isAuthenticated && token) {
      try {
        await axios.patch(
          `${process.env.REACT_APP_BACKEND_URL}/api/cart/${itemId}`,
          { quantity },
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        dispatch({ type: 'UPDATE_ITEM', payload: { id: itemId, quantity } });
      } catch (error) {
        console.error('Failed to update quantity:', error);
      }
    } else {
      dispatch({ type: 'UPDATE_ITEM', payload: { id: itemId, quantity } });
    }
  };

  const removeFromCart = async (itemId) => {
    if (isAuthenticated && token) {
      try {
        await axios.delete(
          `${process.env.REACT_APP_BACKEND_URL}/api/cart/${itemId}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        dispatch({ type: 'REMOVE_ITEM', payload: itemId });
      } catch (error) {
        console.error('Failed to remove from cart:', error);
      }
    } else {
      dispatch({ type: 'REMOVE_ITEM', payload: itemId });
    }
  };

  const clearCart = () => {
    dispatch({ type: 'CLEAR_CART' });
    localStorage.removeItem('guestCart');
  };

  const getCartTotal = () => {
    return state.items.reduce(
      (total, item) => total + item.product.price * item.quantity,
      0
    );
  };

  const getCartCount = () => {
    return state.items.reduce((count, item) => count + item.quantity, 0);
  };

  return (
    <CartContext.Provider
      value={{
        items: state.items,
        addToCart,
        updateQuantity,
        removeFromCart,
        clearCart,
        getCartTotal,
        getCartCount,
        syncGuestCart,
      }}
    >
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within CartProvider');
  }
  return context;
};