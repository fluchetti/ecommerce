import { useContext } from "react";
import { Product } from "../components/Product";
import ProductsContext from "../context/ProductsContext";

export const Products = () => {
  const { products, loadMoreProducts } = useContext(ProductsContext);
  return (
    <div className="container">
      <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
        {products.results &&
          products.results.map((product) => (
            <div key={product.id} className="col">
              <Product data={product} />
            </div>
          ))}
      </div>
      {products.next && (
        <div className="text-center">
          <button className="btn btn-primary my-3 " onClick={loadMoreProducts}>
            Get more products
          </button>
        </div>
      )}
    </div>
  );
};

export default Products;
