import { createContext, useReducer } from "react";
import { cartReducer, initialCart } from "../reducers/cartReducer";

const CartContext = createContext();

const CartProvider = ({ children }) => {
  const [cartState, dispatch] = useReducer(cartReducer, initialCart);

  return (
    <CartContext.Provider value={{ cartState, dispatch }}>
      {children}
    </CartContext.Provider>
  );
};

export { CartProvider };
export default CartContext;
