import { useContext, useState } from "react";
import AuthContext from "../context/AuthContext";

export const LoginForm = () => {
  const { login } = useContext(AuthContext);
  const [form, setForm] = useState({ email: "", password: "" });
  const handleSubmit = (e) => {
    e.preventDefault();
    login(form.email, form.password);
  };
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
  return (
    <form onSubmit={handleSubmit} className="p-3">
      <div className="mb-3">
        <input
          type="email"
          placeholder="Email"
          name="email"
          required
          value={form.email}
          onChange={handleChange}
          className="form-control"
        />
      </div>
      <div className="mb-3">
        <input
          type="password"
          placeholder="Contraseña"
          name="password"
          required
          value={form.password}
          onChange={handleChange}
          className="form-control"
        />
      </div>
      <button type="submit" className="btn btn-primary">
        Iniciar sesión
      </button>
    </form>
  );
};

export default LoginForm;
