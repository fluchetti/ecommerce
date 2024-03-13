import { useContext, useEffect } from "react";

import AuthContext from "../context/AuthContext";
import ProductCreateForm from "../components/ProductCreateForm";
import { useNavigate } from "react-router-dom";

export const ProductCreate = () => {
  const { authTokens } = useContext(AuthContext);
  const navigate = useNavigate();
  useEffect(() => {
    if (authTokens === null) {
      navigate("/login");
      return;
    }
  }, [authTokens]);

  return (
    <div className="container my-2">
      <h3 className="text-center">Crear producto</h3>
      <div className="container my-5">
        <ProductCreateForm></ProductCreateForm>
      </div>
    </div>
  );
};

export default ProductCreate;
