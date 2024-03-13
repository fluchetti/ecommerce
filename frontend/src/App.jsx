import { BrowserRouter, Route, Routes } from "react-router-dom";
import Landing from "./pages/Landing";
import NotFound from "./pages/NotFound";
import { Profile } from "./pages/Profile";
import Categories from "./pages/Categories";
import NavBar from "./layouts/NavBar";
import { Footer } from "./layouts/Footer";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "bootstrap-icons/font/bootstrap-icons.css";
import "./App.css";
import { CategoryDetail } from "./pages/CategoryDetail";
import { ProductsProvider } from "./context/ProductsContext";
import ProductDetail from "./pages/ProductDetail";
import { CategoriesProvider } from "./context/CategoriesContext";
import { CartProvider } from "./context/CartContext";
import CartDetail from "./pages/CartDetail";
import { AuthProvider } from "./context/AuthContext";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Posts from "./pages/Posts";
import ProfileEdit from "./pages/ProfileEdit";
import ProductEdit from "./pages/ProductEdit";
import ProductCreate from "./pages/ProductCreate";
import ChangePassword from "./pages/ChangePassword";
import Compras from "./pages/Compras";
function App() {
  return (
    <>
      <BrowserRouter>
        <AuthProvider>
          <CartProvider>
            <CategoriesProvider>
              <ProductsProvider>
                <NavBar></NavBar>
                <Routes>
                  <Route path="/" element={<Landing></Landing>}></Route>
                  <Route
                    path="/products/create"
                    element={<ProductCreate></ProductCreate>}
                  ></Route>
                  <Route
                    path="/products/:slug"
                    element={<ProductDetail></ProductDetail>}
                  ></Route>
                  <Route
                    path="/products/edit/:slug"
                    element={<ProductEdit></ProductEdit>}
                  ></Route>
                  <Route
                    path="/profile/edit"
                    element={<ProfileEdit></ProfileEdit>}
                  ></Route>
                  <Route
                    path="/profile/change_password"
                    element={<ChangePassword></ChangePassword>}
                  ></Route>
                  <Route
                    path="/profile/:slug"
                    element={<Profile></Profile>}
                  ></Route>

                  <Route path="/login" element={<Login></Login>}></Route>
                  <Route path="/signup" element={<Signup></Signup>}></Route>
                  <Route path="/posts" element={<Posts></Posts>}></Route>
                  <Route path="/compras" element={<Compras></Compras>}></Route>
                  <Route
                    path="/categories"
                    element={<Categories></Categories>}
                  ></Route>
                  <Route
                    path="/categories/:slug"
                    element={<CategoryDetail></CategoryDetail>}
                  ></Route>
                  <Route
                    path="/cart"
                    element={<CartDetail></CartDetail>}
                  ></Route>
                  <Route path="*" element={<NotFound></NotFound>}></Route>
                </Routes>
                <Footer></Footer>
              </ProductsProvider>
            </CategoriesProvider>
          </CartProvider>
        </AuthProvider>
      </BrowserRouter>
    </>
  );
}

export default App;
