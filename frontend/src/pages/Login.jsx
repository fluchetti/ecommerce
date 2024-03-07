import { useContext } from "react";
import LoginForm from "../components/LoginForm";
import AuthContext from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export const Login = () => {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  if (user) {
    navigate("/");
  }
  return (
    <div className="container text-center">
      {<LoginForm></LoginForm>}
      <p>
        No tenes una cuenta? <a href="/signup">Registrate</a>
      </p>
    </div>
  );
};

export default Login;
