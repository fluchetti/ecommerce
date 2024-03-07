import { useContext, useEffect, useState } from "react";
import { NavLink, useNavigate, useParams } from "react-router-dom";
import ProductsContext from "../context/ProductsContext";
import { helpHttp } from "../helpers/helpHttp";
import { TPYES } from "../actions/cartActions";
import CartContext from "../context/CartContext";
import AuthContext from "../context/AuthContext";

export const ProductDetail = () => {
  const { error, setError } = useContext(ProductsContext);
  const { user, authTokens } = useContext(AuthContext);
  const { slug } = useParams();
  const [product, setProduct] = useState(null);
  const [loadingProduct, setLoadingProduct] = useState(true);
  const { dispatch } = useContext(CartContext);
  const [adding, setAdding] = useState(false);
  const navigate = useNavigate();
  let api = helpHttp();
  useEffect(() => {
    api.get(`http://127.0.0.1:8000/api/products/detail/${slug}`).then((res) => {
      if (!res.err) {
        setProduct(res);
        setError(null);
        console.log(res);
      } else {
        setError(res.err);
      }
      setLoadingProduct(false);
    });
  }, [slug]);

  // Add to cart
  const addToCart = () => {
    console.log("mando a añadir a , ", product);
    dispatch({ type: TPYES.ADD_TO_CART, payload: product });
  };
  // Buy product
  const buyProduct = () => {
    dispatch({ type: TPYES.ADD_TO_CART, payload: product });
    navigate("/cart");
  };
  // Delete producto
  const handleDelete = () => {
    const isConfirmed = window.confirm("¿Borrar publicación?");
    if (isConfirmed) {
      fetch(`http://127.0.0.1:8000/api/products/detail/${slug}`, {
        headers: { Authorization: `Bearer ${authTokens.access}` },
        method: "DELETE",
      })
        .then((res) => {
          if (res.ok) {
            console.log("Producto eliminado correctamente");
            navigate("/posts");
          } else {
            console.error("Error al eliminar el producto");
          }
        })
        .catch((error) => {
          console.error("Error al eliminar el producto:", error);
        });
    }
  };

  if (loadingProduct) {
    return <div>Cargando</div>;
  }
  // Verificar si hay un error
  if (error) {
    return <div>Ocurrió un error al cargar los datos: {error.statusText}</div>;
  }
  // Verificar si el producto estan cargado y no es null
  if (!product) {
    return <div>No se encontró el producto</div>;
  }
  // Renderizar los detalles del producto
  return (
    <div className="container  my-5">
      <div className="row">
        <div className="col-md-6">
          <img
            src={`http://127.0.0.1:8000${product.image}`}
            className="d-block w-100"
            alt={product.title}
          />
        </div>
        <div className="col-md-6  py-5 px-5">
          <div className="d-flex flex-column h-100 justify-content-between">
            <div>
              <h2 className="mb-4 text-center">{product.title}</h2>
              {product.discount_percentage > 0 ? (
                <p className="card-text">
                  $<del>{product.price}</del> ${product.discount_value}
                </p>
              ) : (
                <p className="card-text">${product.price} </p>
              )}
              {product.discount_percentage > 0 && (
                <p style={{ color: "green" }}>
                  {product.discount_percentage}% OFF
                </p>
              )}
              <p>{product.summary}</p>
              <NavLink
                className="text-muted"
                to={`/profile/${product.owner_slug}`}
              >
                Vendido por: {product.owner}
              </NavLink>
              <br />
              <NavLink
                className="text-muted"
                to={`/categories/${product.category_slug}`}
              >
                Categoria: {product.category_slug}
              </NavLink>
            </div>
            {user && product.owner_id == user.user_id ? (
              <div className="d-flex flex-column">
                <NavLink
                  className="btn btn-primary mb-3"
                  to={`/products/edit/${product.slug}`}
                >
                  Editar
                </NavLink>
                <button className="btn btn-danger mb-3" onClick={handleDelete}>
                  Borrar
                </button>
              </div>
            ) : (
              <div className="d-flex flex-column">
                <button
                  className="btn btn-primary mb-3"
                  disabled={user ? false : true}
                  onClick={buyProduct}
                >
                  Comprar
                </button>
                <button
                  className="btn btn-secondary mb-3"
                  onClick={addToCart}
                  disabled={user ? false : true}
                >
                  {adding ? "Añadiendo al carrito.." : "Añadir al carrito"}
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
      <div className="row">
        <div className="col">
          <p>{product.description}</p>
        </div>
      </div>
    </div>
  );
};

export default ProductDetail;
