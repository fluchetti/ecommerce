import { Link } from "react-router-dom";

export const Product = ({ data }) => {
  let {
    category_slug,
    title,
    price,
    slug,
    image,
    discount_value,
    discount_percentage,
  } = data;
  return (
    <div className="card h-100">
      <img
        src={`http://127.0.0.1:8000${image}`}
        className="card-img-top"
        alt=""
      />
      <div className="card-body">
        <Link to={`/products/${slug}`} className="card-title">
          {title}
        </Link>
        {discount_percentage > 0 ? (
          <p className="card-text">
            $<del>{price}</del> ${discount_value}{" "}
          </p>
        ) : (
          <p className="card-text">${price} </p>
        )}
      </div>
      <div className="card-footer text-end">
        {discount_percentage > 0 && (
          <small
            className="mx-2"
            style={{ color: "green", fontWeight: "bold" }}
          >
            {discount_percentage}% off{" "}
          </small>
        )}
        <Link to={`/categories/${category_slug}`}>{category_slug}</Link>
      </div>
    </div>
  );
};

export default Product;
