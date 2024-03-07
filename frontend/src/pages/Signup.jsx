import SignupForm from "../components/SignupForm";

export const Signup = () => {
  return (
    <div className="container">
      <div className="row justify-content-center mt-5">
        <div className="col-lg-6">
          <h2 className="mt-4">Registro de usuario</h2>
          <SignupForm></SignupForm>
        </div>
      </div>
    </div>
  );
};

export default Signup;
