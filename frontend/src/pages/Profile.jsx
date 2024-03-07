import { useContext, useEffect, useState } from "react";
import AuthContext from "../context/AuthContext";
import { helpHttp } from "../helpers/helpHttp";
import { ProfileCard } from "../components/ProfileCard";
import { useParams } from "react-router-dom";

export const Profile = () => {
  const { user, authTokens, logout } = useContext(AuthContext);
  const [loadingProfile, setLoadingProfile] = useState(false);
  const [userProfile, setUserProfile] = useState(null);
  let { slug } = useParams();
  let api = helpHttp();
  // Aca tendria que fetchear los datos del usuario valiendome de user.slug.
  // Si el token de access expiro y entro directo a esta pagina no me autoriza a hacer el fetch.
  useEffect(() => {
    api
      .get(`http://127.0.0.1:8000/api/users/${slug}`, {
        headers: { Authorization: `Bearer ${authTokens?.access}` },
      })
      .then((res) => {
        setUserProfile(res);
      })
      .catch((error) => {
        console.log("ocurrio un error ", authTokens.access);
        setLoadingProfile(false);
        logout();
      })
      .finally(() => {
        setLoadingProfile(false);
      });
  }, [slug]);

  const deleteAccount = () => {
    api
      .del(`http://127.0.0.1:8000/api/users/${slug}`, {
        headers: {
          Authorization: `Bearer ${authTokens.access}`,
        },
      })
      .then((res) => {
        console.log(res);
        alert(res.message);
        logout();
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <>
      {loadingProfile && <p>Carando datos del perfil...</p>}
      {userProfile && (
        <ProfileCard
          deleteAccount={deleteAccount}
          userProfile={userProfile}
          user={user}
        ></ProfileCard>
      )}
    </>
  );
};
