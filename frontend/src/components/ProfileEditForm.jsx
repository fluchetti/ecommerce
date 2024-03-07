import { useState } from "react";
import { useNavigate } from "react-router-dom";

export const ProfileEditForm = ({ data, authTokens }) => {
  const [form, setForm] = useState(data);
  const navigate = useNavigate();
  const handleSubmit = (e) => {
    e.preventDefault();
    let form_data = new FormData();
    if (form.avatar instanceof File) {
      form_data.append("avatar", form.avatar);
    }
    form_data.append("bio", form.bio);
    form_data.append("first_name", form.first_name);
    form_data.append("last_name", form.last_name);
    form_data.append("birthday", form.birthday);
    form_data.append("phone", form.phone);
    fetch(`http://127.0.0.1:8000/api/users/${form.slug}`, {
      method: "PUT",
      headers: {
        Accept: "application/json",

        Authorization: `Bearer ${authTokens.access}`,
      },
      body: form_data,
    })
      .then((res) => {
        if (res.ok) {
          return res.json();
        }
      })
      .then((json) => {
        navigate("/profile");
      })
      .catch((error) => {
        console.log(error);
      });
  };

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
  return (
    <form onSubmit={handleSubmit}>
      <div className="mb-3">
        <label htmlFor="avatar" className="form-label me-5">
          Avatar
        </label>
        <img src={`http://127.0.0.1:8000${form.avatar}`} alt="" />
        <input
          type="file"
          className="form-control"
          id="avatar"
          name="avatar"
          onChange={handleImageChange}
        />
      </div>
      <div className="mb-3">
        <label htmlFor="bio" className="form-label">
          Bio
        </label>
        <textarea
          className="form-control"
          id="bio"
          name="bio"
          value={form.bio || ""}
          onChange={handleChange}
        ></textarea>
      </div>
      <div className="mb-3">
        <label htmlFor="first_name" className="form-label">
          Nombre
        </label>
        <input
          type="text"
          className="form-control"
          id="first_name"
          name="first_name"
          value={form.first_name}
          onChange={handleChange}
        />
      </div>
      <div className="mb-3">
        <label htmlFor="last_name" className="form-label">
          Apellido
        </label>
        <input
          type="text"
          className="form-control"
          id="last_name"
          name="last_name"
          value={form.last_name}
          onChange={handleChange}
        />
      </div>
      <div className="mb-3">
        <label htmlFor="last_name" className="form-label">
          Nacimiento
        </label>
        <input
          type="date"
          className="form-control"
          id="birthday"
          name="birthday"
          value={form.birthday}
          onChange={handleChange}
        />
      </div>
      <div className="mb-3">
        <label htmlFor="phone" className="form-label">
          Teléfono
        </label>
        <input
          type="text"
          className="form-control"
          id="phone"
          name="phone"
          value={form.phone}
          onChange={handleChange}
        />
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

export default ProfileEditForm;
