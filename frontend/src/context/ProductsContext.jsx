// ProductContext.js
import { createContext, useEffect, useState } from "react";
import { helpHttp } from "../helpers/helpHttp";
import { useSearchParams } from "react-router-dom";

const ProductsContext = createContext();

const ProductsProvider = ({ children }) => {
  const [products, setProducts] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchParams] = useSearchParams();
  let api = helpHttp();
  useEffect(() => {
    setLoading(true);
    const queryParams = new URLSearchParams(searchParams);
    const title = queryParams.get("title");
    api
      .get(
        title
          ? `http://127.0.0.1:8000/api/products/list?title=${title}`
          : "http://127.0.0.1:8000/api/products/list"
      )
      .then((res) => {
        if (!res.err) {
          setProducts(res);
          setError(null);
        } else {
          setError(res.err);
          setProducts(null);
        }
        setLoading(false);
      })
      .catch((error) => {
        setError(error);
        setProducts(null);
        setLoading(false);
      });
  }, [searchParams]);

  const loadMoreProducts = () => {
    setLoading(true);
    api
      .get(products.next)
      .then((res) => {
        if (!res.err) {
          setProducts({
            ...res,
            results: [...products.results, ...res.results],
          });
        } else {
          setError(res.err);
          setProducts(null);
        }
        setLoading(false);
      })
      .catch((error) => {
        setError(error);
        setProducts(null);
        setLoading(false);
      });
  };

  const data = {
    products,
    loading,
    error,
    loadMoreProducts,
    setLoading,
    setError,
  };

  return (
    <ProductsContext.Provider value={data}>{children}</ProductsContext.Provider>
  );
};

export { ProductsProvider };
export default ProductsContext;
