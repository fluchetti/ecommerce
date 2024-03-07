import { useParams } from "react-router-dom";
import { helpHttp } from "../helpers/helpHttp";
import { useEffect, useState } from "react";
import Product from "../components/Product";

export const CategoryDetail = () => {
  const [category, setCategory] = useState(null);
  const [relatedProducts, setRelatedProducts] = useState([]);
  const [error, setError] = useState(false);
  const { slug } = useParams();
  let api = helpHttp();

  const getCategory = () => {
    api
      .get(`http://127.0.0.1:8000/api/categories/${slug}`)
      .then((res) => {
        if (!res.err) {
          setCategory(res);
          // Una vez que obtengas los detalles de la categoría, obtén los productos relacionados
          getRelatedProducts(res.id);
        } else {
          setError(true);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        setError(true);
      });
  };

  const getRelatedProducts = (categoryId) => {
    // Realiza una solicitud al backend para obtener los productos relacionados con la categoría
    api
      .get(`http://127.0.0.1:8000/api/products/list/${categoryId}`)
      .then((res) => {
        if (!res.err) {
          setRelatedProducts(res);
        } else {
          setError(true);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        setError(true);
      });
  };

  useEffect(() => {
    getCategory();
  }, [slug]);

  if (error) {
    return <div>Ocurrio un error</div>;
  }
  return (
    <>
      <div className="container">
        {category && (
          <div className="my-2 p-4">
            <h2 className="text-center mb-4">{category.name} </h2>
            <div className="row ">
              <img
                className="col-6"
                src={`http://127.0.0.1:8000${category.image}`}
                alt=""
              />
              <p className="col-6">{category.description} </p>
            </div>
          </div>
        )}
        <h6 className="text-center py-3">Related products</h6>
        <div className="row">
          {relatedProducts.length > 0 &&
            relatedProducts.map((product) => (
              <div className="col-md-3 mb-3" key={product.id}>
                <Product data={product} />
              </div>
            ))}
        </div>
      </div>
    </>
  );
};

export default CategoryDetail;
