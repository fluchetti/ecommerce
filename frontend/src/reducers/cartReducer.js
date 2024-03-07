import { TPYES } from "../actions/cartActions";

export const initialCart = { cartItems: [] };

export function cartReducer(state, action) {
  switch (action.type) {
    case TPYES.ADD_TO_CART: {
      console.log(action.payload);
      // Tengo que ver si ya esta en el cart
      const itemInCart = state.cartItems.find(
        (item) => item.id === action.payload.id
      );
      console.log(itemInCart);
      // Si esta en el cart aumento su cantidad en 1. Si no esta simplemente lo agrego con cantidad 1.
      return itemInCart
        ? // Esta
          {
            ...state,
            cartItems: state.cartItems.map((item) =>
              item.id !== action.payload.id
                ? item
                : { ...item, quantity: item.quantity + 1 }
            ),
          }
        : // No esta
          {
            ...state,
            cartItems: [...state.cartItems, { ...action.payload, quantity: 1 }],
          };
    }

    case TPYES.REMOVE_ONE_FROM_CART: {
      const itemToRemove = state.cartItems.find(
        (item) => item.id === action.payload.id
      );
      console.log(itemToRemove);
      return itemToRemove.quantity === 1
        ? {
            ...state,
            cartItems: state.cartItems.filter(
              (item) => item.id !== action.payload.id
            ),
          }
        : {
            ...state,
            cartItems: state.cartItems.map((item) =>
              item.id === action.payload.id
                ? { ...item, quantity: item.quantity - 1 }
                : { ...item }
            ),
          };
    }
    case TPYES.REMOVE_ALL_FROM_CART: {
      return {
        ...state,
        cartItems: state.cartItems.filter(
          (item) => item.id !== action.payload.id
        ),
      };
    }

    case TPYES.CONFIRM_CLEAR_CART: {
      const isConfirmed = window.confirm("Borrar carrito de compras?");
      if (isConfirmed) {
        return { ...state, cartItems: initialCart.cartItems };
      } else {
        return state;
      }
    }

    case TPYES.CLEAR_CART: {
      return { ...state, cartItems: initialCart.cartItems };
    }
  }
}
