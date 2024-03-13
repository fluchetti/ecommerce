import { useContext, useEffect, useState } from "react";
import AuthContext from "../context/AuthContext";
import { helpHttp } from "../helpers/helpHttp";
import { useNavigate } from "react-router-dom";

const initialForm = {
  title: "",
  description: "",
  summary: "",
  price: "",
  discount_percentage: "",
  category: "1",
  image: "",
  status: "published",
};

export const ProductCreateForm = () => {
  const { authTokens } = useContext(AuthContext);
  const [form, setForm] = useState(initialForm);
  const [categories, setCategories] = useState([]);
  const [message, setMessage] = useState({ type: null, msg: "" });
  const navigate = useNavigate();
  let api = helpHttp();
  useEffect(() => {
    api.get("http://127.0.0.1:8000/api/categories/all").then((res) => {
      if (!res.err) {
        setCategories(res);
      }
    });
  }, []);

  const handleDiscard = () => {
    setForm(initialForm);
  };
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
  const handleImageChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.files[0] });
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    let form_data = new FormData();
    if (form.image instanceof File) {
      form_data.append("image", form.image);
    }
    form_data.append("title", form.title);
    form_data.append("description", form.description);
    form_data.append("summary", form.summary);
    form_data.append("price", form.price);
    form_data.append("discount_percentage", form.discount_percentage);
    form_data.append("category", form.category);
    form_data.append("status", form.status || "published");
    fetch("http://127.0.0.1:8000/api/products/create", {
      method: "POST",
      headers: {
        Accept: "application/json",

        Authorization: `Bearer ${authTokens.access}`,
      },
      body: form_data,
    })
      .then((res) => {
        console.log(res);
        if (res.ok) {
          return res.json();
        }
      })
      .then((json) => {
        console.log(json);
        setMessage({
          type: "success",
          msg: "Producto creado correctamente. Estas siendo redireccionado.",
        });
        setForm(initialForm);
        setTimeout(() => {
          navigate("/posts");
        }, 3000);
      })
      .catch((error) => {
        console.log(error);
        setMessage({ type: "danger", msg: "Ocurrió un error" });
      });
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="title" className="form-label">
            Título
          </label>
          <input
            type="text"
            className="form-control"
            name="title"
            value={form.title}
            onChange={handleChange}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="summary" className="form-label">
            Resumen
          </label>
          <textarea
            className="form-control"
            name="summary"
            rows="3"
            value={form.summary}
            onChange={handleChange}
          ></textarea>
        </div>
        <div className="mb-3">
          <label htmlFor="description" className="form-label">
            Descripción
          </label>
          <textarea
            className="form-control"
            name="description"
            rows="5"
            value={form.description}
            onChange={handleChange}
          ></textarea>
        </div>
        <div className="mb-3">
          <label htmlFor="price" className="form-label">
            Precio
          </label>
          <input
            type="number"
            className="form-control"
            name="price"
            value={form.price}
            onChange={handleChange}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="discountPercentage" className="form-label">
            Porcentaje de Descuento
          </label>
          <input
            type="number"
            className="form-control"
            name="discount_percentage"
            value={form.discount_percentage}
            onChange={handleChange}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="category" className="form-label">
            Categoría
          </label>
          <select
            className="form-select"
            name="category"
            value={form.category}
            onChange={handleChange}
          >
            <option value="">Seleccionar categoría</option>
            {categories.length > 0 &&
              categories.map((category) => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
          </select>
        </div>
        <div className="mb-3">
          <label htmlFor="image" className="form-label">
            Imagen
          </label>
          <input
            type="file"
            className="form-control"
            accept="image/jpeg,image/png"
            name="image"
            onChange={handleImageChange}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="status" className="form-label">
            Estado
          </label>
          <select
            className="form-select"
            name="status"
            value={form.status}
            onChange={handleChange}
          >
            <option value="published">Publicado</option>
            <option value="paused">Pausado</option>
          </select>
        </div>
        <input
          type="submit"
          className="btn btn-primary me-2"
          value={"Publicar"}
        />
        <button className="btn btn-primary mx-2" onClick={handleDiscard}>
          Cancelar
        </button>
      </form>
      <div>
        {message.type && (
          <div
            className={`alert alert-${message.type} alert-dismissible fade show text-center mt-3`}
          >
            {message.msg}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductCreateForm;
