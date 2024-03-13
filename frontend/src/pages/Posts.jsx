import { useContext, useEffect, useState } from "react";
import { helpHttp } from "../helpers/helpHttp";
import Product from "../components/Product";
import AuthContext from "../context/AuthContext";
import { NavLink, useNavigate } from "react-router-dom";
export const Posts = () => {
  const { authTokens } = useContext(AuthContext);
  const [products, setProducts] = useState([]);
  const api = helpHttp();
  const navigate = useNavigate();
  useEffect(() => {
    if (authTokens === null) {
      navigate("/login");
      return;
    }
    api
      .get(`http://127.0.0.1:8000/api/users/posts`, {
        headers: { Authorization: `Bearer ${authTokens.access}` },
      })
      .then((res) => {
        setProducts(res);
      });
  }, [authTokens]);

  return (
    <div className="container">
      <h3 className="text-center">Tus publicaciones</h3>
      <div className="row row-cols-1 row-cols-md-3 g-4">
        {products.length > 0 ? (
          products.map((product) => (
            <div key={product.id} className="col">
              <Product data={product} status={product.status} />
            </div>
          ))
        ) : (
          <p className="text-center">No tenes productos publicados.</p>
        )}
      </div>
      <div className="mt-2 mb-5 text-center">
        <NavLink to={"/products/create"}>Crear nuevo producto</NavLink>
      </div>
    </div>
  );
};

export default Posts;
