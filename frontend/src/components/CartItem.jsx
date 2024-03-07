import { useContext } from "react";
import CartContext from "../context/CartContext";
import { TPYES } from "../actions/cartActions";

export const CartItem = ({ data }) => {
  const { title, summary, quantity, discount_value } = data;
  const { dispatch } = useContext(CartContext);
  const finalPrice = parseFloat(discount_value) * parseFloat(quantity);
  const deleteItem = ({ all = false }) => {
    if (all) {
      dispatch({ type: TPYES.REMOVE_ALL_FROM_CART, payload: data });
    } else {
      dispatch({ type: TPYES.REMOVE_ONE_FROM_CART, payload: data });
    }
  };
  return (
    <div>
      <div className="container my-2">
        <h3 className="text-center">{`${quantity}x ${title}`}</h3>
        <p>{summary}</p>
        <p>Total: {finalPrice}</p>
        <button onClick={deleteItem} className="btn btn-danger m-2">
          Borrar uno
        </button>
        <button
          onClick={() => deleteItem({ all: true })}
          className="btn btn-danger m-2"
        >
          Borrar todos
        </button>
      </div>
    </div>
  );
};

export default CartItem;
