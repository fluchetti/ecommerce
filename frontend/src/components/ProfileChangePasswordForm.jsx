import { useContext, useState } from "react";
import { helpHttp } from "../helpers/helpHttp";
import AuthContext from "../context/AuthContext";

const initialForm = { password: "", password2: "" };

const ProfileChangePasswordForm = () => {
  const [form, setForm] = useState(initialForm);
  const { authTokens } = useContext(AuthContext);
  const [message, setMessage] = useState(null);
  let api = helpHttp();
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (form.password === form.password2) {
      // Realizar el cambio de contraseña
      api
        .post("http://127.0.0.1:8000/api/users/change_password", {
          body: form,
          headers: {
            Authorization: `Bearer ${authTokens.access} `,
            "Content-type": "application/json",
          },
          method: "POST",
        })
        .then((res) => {
          console.log(res);
          console.log("Contraseña cambiada exitosamente");
          setMessage("Contraseña cambiada exitosamente");
        })
        .catch((error) => {
          console.log(error);
          setMessage("Ocurrio un error al cambiar la contraseña");
        });
    } else {
      console.log("Las contraseñas no coinciden");
    }
    // Limpiar los campos de entrada después de enviar el formulario
    setForm;
  };

  return (
    <div className="container d-flex justify-content-center my-5">
      <form onSubmit={handleSubmit} className="mt-4 w-50">
        <div className="mb-3">
          <label htmlFor="password" className="form-label">
            Nueva contraseña:
          </label>
          <input
            type="password"
            className="form-control"
            id="password"
            value={form.password}
            name="password"
            onChange={handleChange}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password2" className="form-label">
            Confirmar contraseña:
          </label>
          <input
            type="password"
            className="form-control"
            id="password2"
            value={form.password2}
            name="password2"
            onChange={handleChange}
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Cambiar contraseña
        </button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default ProfileChangePasswordForm;
