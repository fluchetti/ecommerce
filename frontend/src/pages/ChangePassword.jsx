import ProfileChangePasswordForm from "../components/ProfileChangePasswordForm";
import { Navigate } from "react-router-dom";
import AuthContext from "../context/AuthContext";
import { useContext } from "react";

export const ChangePassword = () => {
  const { authTokens } = useContext(AuthContext);
  if (!authTokens) {
    return <Navigate to="/" />;
  }

  return (
    <div className="container">
      <h3>Cambiar contraseña</h3>
      <ProfileChangePasswordForm></ProfileChangePasswordForm>
    </div>
  );
};

export default ChangePassword;
