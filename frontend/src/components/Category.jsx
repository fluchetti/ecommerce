import { Link } from "react-router-dom";

export const Category = ({ data }) => {
  const { name, description, slug } = data;
  return (
    <div className="container  py-2 my-2">
      <Link
        to={`/categories/${slug}`}
        className="card-title"
        style={{ textDecoration: "none" }}
      >
        <h3>{name}</h3>
      </Link>
      <p>{description}</p>
    </div>
  );
};

export default Category;
