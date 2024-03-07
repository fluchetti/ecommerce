import { useContext, useState } from "react";
import { Link, NavLink, useNavigate, useSearchParams } from "react-router-dom";
import CategoriesContext from "../context/CategoriesContext";
import AuthContext from "../context/AuthContext";

export const NavBar = () => {
  // Esto se renderiza cada vez que cambio de pagina.
  const { categories } = useContext(CategoriesContext);
  const { user, logout } = useContext(AuthContext);
  const [title, setTitle] = useState("");
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  const handleChange = (e) => {
    e.preventDefault();
    setTitle(e.target.value);
  };
  const handleSearch = (e) => {
    e.preventDefault();
    setSearchParams({ title: title });
    navigate(`/?title=${title}`);
    setTitle("");
  };
  return (
    <>
      <nav className="navbar navbar-expand-lg bg-light">
        <div className="container-fluid">
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <NavLink to="/" className="nav-link">
                  Ecommerce
                </NavLink>
              </li>
              {user ? (
                <li className="nav-item dropdown">
                  <a
                    className="nav-link dropdown-toggle"
                    href="#"
                    role="button"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                  >
                    Perfil
                  </a>
                  <ul className="dropdown-menu">
                    <li>
                      <NavLink
                        to={`/profile/${user.slug}`}
                        className="dropdown-item"
                      >
                        Ver perfil
                      </NavLink>
                    </li>
                    <li>
                      <NavLink to="/posts" className="dropdown-item">
                        Ver publicaciones
                      </NavLink>
                    </li>
                    <li>
                      <NavLink to="/compras" className="dropdown-item">
                        Ver compras
                      </NavLink>
                    </li>
                    <li>
                      <a className="dropdown-item" onClick={logout}>
                        Logout
                      </a>
                    </li>
                  </ul>
                </li>
              ) : (
                <li className="nav-item">
                  <NavLink to="/login" className="nav-link">
                    Login
                  </NavLink>
                </li>
              )}

              <li className="nav-item dropdown">
                <a
                  className="nav-link dropdown-toggle"
                  href="#"
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  Categories
                </a>
                <ul className="dropdown-menu">
                  {categories &&
                    categories.map((categoria) => (
                      <li key={categoria.id}>
                        <Link
                          to={`/categories/${categoria.slug}`}
                          className="dropdown-item"
                        >
                          {categoria.name}
                        </Link>
                      </li>
                    ))}
                  <li>
                    <hr className="dropdown-divider" />
                  </li>
                  <li>
                    <NavLink to="/categories" className="nav-link">
                      Ver mas
                    </NavLink>
                  </li>
                </ul>
              </li>
              {user && (
                <li className="nav-item">
                  <NavLink to="/cart" className="nav-link">
                    <i className="bi bi-cart"></i>
                  </NavLink>
                </li>
              )}
            </ul>
            <form className="d-flex" role="search">
              <input
                className="form-control me-2"
                type="search"
                placeholder="Buscar titulo.."
                value={title}
                name="title"
                onChange={handleChange}
              />
              <button
                className="btn btn-outline-success"
                type="submit"
                onClick={handleSearch}
              >
                Buscar
              </button>
            </form>
          </div>
        </div>
      </nav>
    </>
  );
};

export default NavBar;
