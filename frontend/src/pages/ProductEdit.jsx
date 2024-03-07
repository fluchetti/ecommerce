import { useContext, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { helpHttp } from "../helpers/helpHttp";
import AuthContext from "../context/AuthContext";
import ProductEditForm from "../components/ProductEditForm";

export const ProductEdit = () => {
  const { slug } = useParams();
  const [product, setProduct] = useState(null);
  const { authTokens } = useContext(AuthContext);
  let api = helpHttp();
  useEffect(() => {
    api
      .get(`http://127.0.0.1:8000/api/products/edit/${slug}`, {
        headers: { Authorization: `Bearer ${authTokens.access}` },
      })
      .then((res) => {
        setProduct(res);
      });
  }, [slug]);

  return (
    <div className="container my-2">
      <h3 className="text-center">Editar producto {slug} </h3>
      {product && (
        <div className="container my-5">
          <ProductEditForm key={product.id} data={product}></ProductEditForm>
        </div>
      )}
    </div>
  );
};

export default ProductEdit;
