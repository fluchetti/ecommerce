import { useContext, useEffect, useState } from "react";
import AuthContext from "../context/AuthContext";
import { helpHttp } from "../helpers/helpHttp";
import PurchaseItem from "../components/PurchaseItem";

export const Compras = () => {
  const [compras, setCompras] = useState([]);
  const { authTokens } = useContext(AuthContext);
  let api = helpHttp();
  useEffect(() => {
    console.log("agarrando tus compras");
    api
      .get(`http://127.0.0.1:8000/api/carts/`, {
        headers: { Authorization: `Bearer ${authTokens.access}` },
      })
      .then((res) => {
        console.log(res);
        setCompras(res);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <div className="container">
      <h3 className="text-center">Tus compras</h3>
      {compras.length > 0 ? (
        compras.map((compra) => (
          <PurchaseItem key={compra.id} purchase={compra}></PurchaseItem>
        ))
      ) : (
        <p>No tenes compras registradas.</p>
      )}
    </div>
  );
};

export default Compras;
