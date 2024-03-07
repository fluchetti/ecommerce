import { useContext, useEffect, useState } from "react";
import AuthContext from "../context/AuthContext";
import { helpHttp } from "../helpers/helpHttp";
import ProfileEditForm from "../components/ProfileEditForm";

export const ProfileEdit = () => {
  const { user, authTokens } = useContext(AuthContext);
  const [userProfile, setUserProfile] = useState(null);
  let api = helpHttp();
  useEffect(() => {
    api
      .get(`http://127.0.0.1:8000/api/users/${user.slug}`, {
        headers: { Authorization: `Bearer ${authTokens.access}` },
      })
      .then((res) => {
        console.log(res);
        setUserProfile(res);
      });
  }, [user]);

  return (
    <div className="container my-3">
      <h3 className="text-center">Editar perfil</h3>
      {userProfile && (
        <ProfileEditForm
          data={userProfile}
          authTokens={authTokens}
        ></ProfileEditForm>
      )}
    </div>
  );
};

export default ProfileEdit;
