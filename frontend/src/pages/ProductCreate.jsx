import { useContext } from "react";

import AuthContext from "../context/AuthContext";
import ProductCreateForm from "../components/ProductCreateForm";

export const ProductCreate = () => {
  const { authTokens } = useContext(AuthContext);
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
