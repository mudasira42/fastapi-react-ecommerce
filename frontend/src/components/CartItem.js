import React from 'react';
import { Trash2, Plus, Minus } from 'lucide-react';
import { useCart } from '../contexts/CartContext';

export const CartItem = ({ item }) => {
  const { updateQuantity, removeFromCart } = useCart();

  const handleQuantityChange = (newQuantity) => {
    if (newQuantity < 1) return;
    updateQuantity(item.id, newQuantity);
  };

  const handleRemove = () => {
    removeFromCart(item.id);
  };

  return (
    <div
      data-testid={`cart-item-${item.id}`}
      className="bg-white rounded-lg p-4 flex items-center space-x-4 shadow-sm border border-gray-100"
    >
      <img
        src={item.product.image}
        alt={item.product.name}
        className="w-20 h-20 object-cover rounded-lg"
      />
      <div className="flex-1">
        <h3
          data-testid={`cart-item-name-${item.id}`}
          className="font-semibold text-gray-900"
        >
          {item.product.name}
        </h3>
        <p className="text-sm text-gray-600">${item.product.price.toFixed(2)}</p>
      </div>
      <div className="flex items-center space-x-3">
        <button
          onClick={() => handleQuantityChange(item.quantity - 1)}
          data-testid={`decrease-quantity-${item.id}`}
          className="p-1 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
        >
          <Minus className="w-4 h-4" />
        </button>
        <span
          data-testid={`cart-item-quantity-${item.id}`}
          className="w-8 text-center font-semibold"
        >
          {item.quantity}
        </span>
        <button
          onClick={() => handleQuantityChange(item.quantity + 1)}
          data-testid={`increase-quantity-${item.id}`}
          className="p-1 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
        >
          <Plus className="w-4 h-4" />
        </button>
      </div>
      <div className="text-right">
        <p
          data-testid={`cart-item-total-${item.id}`}
          className="font-bold text-gray-900 text-lg"
        >
          ${(item.product.price * item.quantity).toFixed(2)}
        </p>
      </div>
      <button
        onClick={handleRemove}
        data-testid={`remove-item-${item.id}`}
        className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
      >
        <Trash2 className="w-5 h-5" />
      </button>
    </div>
  );
};