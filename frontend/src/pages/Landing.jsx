import { useContext } from "react";
import ProductsContext from "../context/ProductsContext";
import Products from "./Products";

export const Landing = () => {
  const { products, error, loading } = useContext(ProductsContext);

  if (error) {
    return <div>Error: {error.err}</div>;
  }

  return (
    <div className="my-4 container">
      {products && <Products />}

      {loading && <div>Cargando....</div>}
    </div>
  );
};

export default Landing;
