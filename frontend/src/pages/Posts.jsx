import { useContext, useEffect, useState } from "react";
import { helpHttp } from "../helpers/helpHttp";
import Product from "../components/Product";
import AuthContext from "../context/AuthContext";
import { NavLink } from "react-router-dom";
export const Posts = () => {
  const { authTokens } = useContext(AuthContext);
  const [products, setProducts] = useState([]);
  const api = helpHttp();
  useEffect(() => {
    api
      .get(`http://127.0.0.1:8000/api/users/posts`, {
        headers: { Authorization: `Bearer ${authTokens.access}` },
      })
      .then((res) => {
        setProducts(res);
      });
  }, []);
  return (
    <div className="container">
      <h3 className="text-center">Tus publicaciones</h3>
      <div className="row row-cols-1 row-cols-md-3 g-4">
        {products.length > 0 ? (
          products.map((product) => (
            <div key={product.id} className="col">
              <Product data={product} />
            </div>
          ))
        ) : (
          <p className="text-center">No hay productos publicados.</p>
        )}
      </div>
      <NavLink to={"/products/create"}>Crear nuevo producto</NavLink>
    </div>
  );
};

export default Posts;
