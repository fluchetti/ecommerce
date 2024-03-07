import { useState } from "react";
import { helpHttp } from "../helpers/helpHttp";
import { useNavigate } from "react-router-dom";

const initialForm = {
  email: "",
  first_name: "",
  last_name: "",
  phone: "",
  birthday: "",
  password: "",
  password2: "",
};

export const SignupForm = () => {
  const [form, setForm] = useState(initialForm);
  const [message, setMessage] = useState(null);
  const navigate = useNavigate();
  let api = helpHttp();
  const handleSubmit = (e) => {
    e.preventDefault();
    // Hacer un put con el form para crear usuario.
    // Valido aca que las contraseñas sean iguales. Si no lo son
    // Seteo las password a defecto y los demas campos los dejo como estaban.
    if (form.password !== form.password2) {
      alert("Las contraseñas no coinciden!");
    }
    const { password2, ...formData } = form;
    api
      .post("http://127.0.0.1:8000/api/users/signup", {
        headers: { "Content-type": "application/json" },
        body: { ...formData },
      })
      .then((res) => {
        console.log(res);
        setForm(initialForm);
        setMessage(true);
        setTimeout(() => {
          navigate("/login");
        }, 3000);
      })
      .catch((error) => {
        console.log("en el catch");
        console.log(error);
        setMessage(error);
      });
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <input
            type="email"
            value={form.email}
            name="email"
            onChange={handleChange}
            className="form-control"
            placeholder="Correo electrónico"
            required
          />
        </div>
        <div className="mb-3">
          <input
            type="text"
            value={form.first_name}
            name="first_name"
            onChange={handleChange}
            className="form-control"
            placeholder="Nombre"
            required
          />
        </div>
        <div className="mb-3">
          <input
            type="text"
            value={form.last_name}
            name="last_name"
            onChange={handleChange}
            className="form-control"
            placeholder="Apellido"
            required
          />
        </div>
        <div className="mb-3">
          <input
            type="text"
            value={form.phone}
            name="phone"
            onChange={handleChange}
            className="form-control"
            placeholder="Telefono"
            required
          />
        </div>
        <div className="mb-3">
          <input
            type="date"
            value={form.birthday}
            name="birthday"
            onChange={handleChange}
            className="form-control"
            placeholder="Fecha de nacimiento"
            required
          />
        </div>
        <div className="mb-3">
          <input
            type="password"
            value={form.password}
            name="password"
            onChange={handleChange}
            className="form-control"
            placeholder="Contraseña"
            required
          />
        </div>
        <div className="mb-3">
          <input
            type="password"
            value={form.password2}
            name="password2"
            onChange={handleChange}
            className="form-control"
            placeholder="Confirmar contraseña"
            required
          />
        </div>
        <div className="d-grid">
          <button type="submit" className="btn btn-primary btn-lg mb-5">
            Registrarme
          </button>
        </div>
      </form>
      {message && <p>{message.statusText}</p>}
    </>
  );
};

export default SignupForm;
