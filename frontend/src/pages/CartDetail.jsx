import { useContext, useEffect, useState } from "react";
import CartContext from "../context/CartContext";
import CartItem from "../components/CartItem";
import { TPYES } from "../actions/cartActions";
import { helpHttp } from "../helpers/helpHttp";
import AuthContext from "../context/AuthContext";
import { Navigate, useNavigate } from "react-router-dom";

export const CartDetail = () => {
  const { cartState, dispatch } = useContext(CartContext);
  const { authTokens } = useContext(AuthContext);
  const [message, setMessage] = useState(null);
  const navigate = useNavigate();
  let api = helpHttp();

  const clearCart = (ask = true) => {
    if (ask) {
      dispatch({ type: TPYES.CONFIRM_CLEAR_CART });
    } else {
      dispatch({ type: TPYES.CLEAR_CART });
    }
  };

  const generateCart = () => {
    console.log(JSON.stringify(cartState.cartItems));
    api
      .post("http://127.0.0.1:8000/api/carts/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${authTokens?.access}`,
          "Content-type": "application/json",
        },
        body: cartState.cartItems,
      })
      .then((res) => {
        console.log(res);
        setMessage("Compra realizada con éxito.");
        setTimeout(() => {
          // Quitar mensaje, llevar cart al estado inicial y redireccionar al inicio.
          setMessage(null);
          clearCart(false);
          navigate("/");
        }, 3000);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  // Verificar si el usuario está autenticado, si no, redirigir al inicio
  if (!authTokens) {
    return <Navigate to="/" />;
  }
  return (
    <div>
      <h4>Cart Detail</h4>
      {cartState.cartItems.length > 0 ? (
        cartState.cartItems.map((cartItem) => (
          <CartItem key={cartItem.id} data={cartItem}></CartItem>
        ))
      ) : (
        <p>No tenes productos en el carrito. Comenza a agregarlos!</p>
      )}
      {cartState.cartItems.length > 0 && (
        <div className=" text-center">
          <button className="btn btn-primary m-2" onClick={generateCart}>
            Realizar compra
          </button>
          <button className="btn btn-danger m-2" onClick={clearCart}>
            Vaciar carro
          </button>
        </div>
      )}
      {message && (
        <div className="w-50 mx-auto mt-2 text-center">
          <h4 className="alert alert-success">{message}</h4>
        </div>
      )}
    </div>
  );
};

export default CartDetail;
