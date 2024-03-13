import { createContext, useEffect, useState } from "react";
import { helpHttp } from "../helpers/helpHttp";
import { jwtDecode } from "jwt-decode";
import { useNavigate } from "react-router-dom";
const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(
    localStorage.getItem("authTokens")
      ? JSON.parse(localStorage.getItem("authTokens"))
      : null
  );
  const [user, setUser] = useState(
    localStorage.getItem("authTokens")
      ? jwtDecode(localStorage.getItem("authTokens"))
      : null
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const api = helpHttp();

  const login = async (email, password) => {
    // Login user. Requiere credenciales de usuario. Si son validas retorna los tokens de acces y refresh.
    try {
      const response = await api.post("http://127.0.0.1:8000/api/token/", {
        headers: { "Content-type": "application/json" },
        body: { email, password },
      });
      setAuthTokens(response);
      localStorage.setItem("authTokens", JSON.stringify(response));
      setUser(jwtDecode(response.access));
      navigate("/");
    } catch (error) {
      console.log("Ocurrio un error en el fetch");
      console.log(error);
      setUser(null);
      setError("Credenciales invalidas");
    }
  };
  const updateTokens = async () => {
    // Refrescar tokens.
    try {
      const response = await api.post(
        "http://127.0.0.1:8000/api/token/refresh/",
        {
          headers: { "Content-type": "application/json" },
          body: { refresh: authTokens.refresh },
        }
      );
      // Si refresco el token me devuelve 2 tokens mas.
      setAuthTokens(response);
      localStorage.setItem("authTokens", JSON.stringify(response));
      setUser(jwtDecode(response.access));
    } catch (error) {
      console.log("Ocurrio un error en el fetch");
      console.log(error);
      setUser(null);
      setAuthTokens(null);
      localStorage.removeItem("authTokens");
    }
    if (loading) {
      setLoading(false);
    }
  };
  const logout = () => {
    // Logout de usuario. Se setean los estados a sus condiciones iniciales y se redirecciona al login
    setUser(null);
    setAuthTokens(null);
    localStorage.removeItem("authTokens");
    navigate("/login");
  };
  // Para refrescar el token de access
  useEffect(() => {
    if (loading) {
      updateTokens();
    }
    let interval = setInterval(() => {
      if (authTokens) {
        updateTokens();
      }
    }, 3600000);
    return () => clearInterval(interval);
  }, [authTokens, loading]);

  const data = { authTokens, login, logout, user, error };
  return (
    <AuthContext.Provider value={data}>
      {loading ? null : children}
    </AuthContext.Provider>
  );
};

export { AuthProvider };
export default AuthContext;
