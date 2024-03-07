import { useContext, useState } from "react";
import { helpHttp } from "../helpers/helpHttp";
import AuthContext from "../context/AuthContext";

export const ProductEditForm = ({ data }) => {
  const { authTokens } = useContext(AuthContext);
  const [form, setForm] = useState(data);
  const handleDiscard = (e) => {
    e.preventDefault();
    setForm(data);
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
    form_data.append("status", form.status);
    fetch(`http://127.0.0.1:8000/api/products/edit/${form.slug}`, {
      method: "PUT",
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
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <form onSubmit={handleSubmit} encType="multipart/form-data">
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
        <input
          type="text"
          className="form-control"
          name="category"
          value={form.category}
          onChange={handleChange}
        />
      </div>
      <div className="mb-3">
        <label htmlFor="image" className="form-label">
          Imagen
        </label>
        <img
          src={`http://127.0.0.1:8000${form.image}`}
          alt="Vista previa de la imagen"
        />
        <input
          type="file"
          className="form-control"
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
        value={"Guardar cambios"}
      />
      <button className="btn btn-primary mx-2" onClick={handleDiscard}>
        Descartar cambios
      </button>
    </form>
  );
};

export default ProductEditForm;
