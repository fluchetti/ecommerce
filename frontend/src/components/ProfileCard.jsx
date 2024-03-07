import { NavLink } from "react-router-dom";
import { helpHttp } from "../helpers/helpHttp";
import { useContext } from "react";
import AuthContext from "../context/AuthContext";

export const ProfileCard = ({ userProfile, deleteAccount, user }) => {
  const { authTokens } = useContext(AuthContext);

  let api = helpHttp();
  const handleDeleteImage = () => {
    console.log("borrando imagen");
    api.del(`http://127.0.0.1:8000/api/users/delete_profile_image`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${authTokens.access}` },
    });
  };

  return (
    <div className="container mt-4 mb-4 p-3 d-flex justify-content-center">
      <div className="card p-4">
        <div className=" image d-flex flex-column justify-content-center align-items-center">
          <img
            src={`http://127.0.0.1:8000${userProfile.avatar}`}
            height="100"
            width="100"
          />
          {userProfile.id === user.user_id && (
            <button className="btn btn-danger mt-3" onClick={handleDeleteImage}>
              Eliminar foto actual
            </button>
          )}
          <span className="name mt-3">
            {userProfile.first_name} {userProfile.last_name}
          </span>
          <span className="idd">Email: {userProfile.email}</span>
          <div className="d-flex flex-row justify-content-center align-items-center gap-2">
            <span className="idd1">Telefono: {userProfile.phone}</span>
            <span>
              <i className="fa fa-copy"></i>
            </span>
          </div>
          <div className="d-flex flex-row justify-content-center align-items-center mt-3">
            <span>{userProfile.bio} </span>
          </div>

          <div className="gap-3 mt-3 icons d-flex flex-row justify-content-center align-items-center">
            <span>
              <i className="bi bi-twitter"></i>
            </span>
            <span>
              <i className="bi bi-facebook"></i>
            </span>
            <span>
              <i className="bi bi-instagram"></i>
            </span>
            <span>
              <i className="bi bi-linkedin"></i>
            </span>
          </div>
          <div className=" px-2 rounded mt-4 date ">
            <span className="join">Joined: {userProfile.created_at}</span>
          </div>
        </div>

        {userProfile.id === user.user_id && (
          <div>
            <NavLink to="/profile/edit" className="btn btn-primary mt-4 mx-2">
              Editar datos
            </NavLink>
            <button
              className="btn btn-danger mt-4 mx-2"
              data-bs-toggle="modal"
              data-bs-target="#exampleModal"
            >
              Borrar cuenta
            </button>
            <p style={{ fontWeight: "bold" }}>
              Cambiar contraseña:{" "}
              <NavLink to="/profile/change_password">Aqui</NavLink>
            </p>
          </div>
        )}

        <div
          className="modal fade"
          id="exampleModal"
          tabIndex="-1"
          aria-labelledby="exampleModalLabel"
          aria-hidden="true"
        >
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h1 className="modal-title fs-5" id="exampleModalLabel">
                  Atencion
                </h1>
                <button
                  type="button"
                  className="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div className="modal-body">
                Vas a borrar tu cuenta. Se perderan todos tus datos.
              </div>
              <div className="modal-footer">
                <button
                  onClick={deleteAccount}
                  type="button"
                  className="btn btn-primary"
                >
                  Confirmar
                </button>
                <button
                  type="button"
                  className="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  Cancelar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
