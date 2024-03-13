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
  confirm_password: "",
};

export const SignupForm = () => {
  const [form, setForm] = useState(initialForm);
  const [message, setMessage] = useState({ message: "", type: "" });
  const navigate = useNavigate();
  let api = helpHttp();
  const handleSubmit = (e) => {
    e.preventDefault();
    // Hacer un put con el form para crear usuario.
    // Valido aca que las contraseñas sean iguales. Si no lo son
    // Seteo las password a defecto y los demas campos los dejo como estaban.
    if (form.password !== form.confirm_password) {
      setForm({ ...form, password: "", confirm_password: "" });
      setMessage("Las contraseñas no coinciden");
      return;
    }
    api
      .post("http://127.0.0.1:8000/api/users/signup", {
        headers: { "Content-type": "application/json" },
        body: { ...form },
      })
      .then((res) => {
        console.log(res);
        setForm(initialForm);
        setMessage({ message: "Usuario creado con exito", type: "success" });
        setTimeout(() => {
          navigate("/login");
        }, 3000);
      })
      .catch((error) => {
        console.log(error);
        setMessage({
          message: "Ocurrio un error al crear el usuario",
          type: "danger",
        });
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
            value={form.confirm_password}
            name="confirm_password"
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
      {message && (
        <p className={`alert alert-${message.type} text-center`}>
          {message.message}
        </p>
      )}
    </>
  );
};

export default SignupForm;
