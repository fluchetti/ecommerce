import { createContext, useEffect, useState } from "react";
import { helpHttp } from "../helpers/helpHttp";

const CategoriesContext = createContext();

const CategoriesProvider = ({ children }) => {
  const [categories, setCategories] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  let api = helpHttp();
  useEffect(() => {
    setLoading(true);
    api.get("http://127.0.0.1:8000/api/categories/").then((res) => {
      if (!res.err) {
        setCategories(res.results);
      } else {
        setError(res.err);
      }
    });
    setLoading(false);
  }, []);

  const data = { categories, error, loading };
  return (
    <CategoriesContext.Provider value={data}>
      {children}
    </CategoriesContext.Provider>
  );
};

export { CategoriesProvider };
export default CategoriesContext;
