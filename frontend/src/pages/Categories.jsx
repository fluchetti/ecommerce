import { useEffect, useState } from "react";
import { helpHttp } from "../helpers/helpHttp";
import Category from "../components/Category";

export const Categories = () => {
  const [categories, setCategories] = useState(null);
  const [error, setError] = useState(false);
  let api = helpHttp();
  useEffect(() => {
    api.get("http://127.0.0.1:8000/api/categories/all").then((res) => {
      if (!res.err) {
        setCategories(res);
      } else {
        setError(true);
      }
    });
  }, []);

  return (
    <>
      {error && <div>Ocurrio un error</div>}
      {categories &&
        categories.map((category) => (
          <Category key={category.id} data={category} />
        ))}
    </>
  );
};

export default Categories;
