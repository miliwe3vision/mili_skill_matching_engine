import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Login() {

const navigate = useNavigate();

const [form, setForm] = useState({
email: "",
password: "",
});

const handleChange = (e) => {
setForm({
...form,
[e.target.name]: e.target.value,
});
};

const handleLogin = async () => {


try {

  const res = await axios.post(
    "http://127.0.0.1:8000/login",
    {
      email: form.email,
      password: form.password,
    }
  );

  const user = res.data.user;

  localStorage.setItem(
    "user",
    JSON.stringify(user)
  );

  if (user.role === "admin") {

    navigate("/admin");

  } else if (user.role === "employee") {

    navigate("/employee");

  }

} catch (error) {

  alert(
    error.response?.data?.detail ||
    "Login Failed"
  );
}


};

return ( <div className="container">


  <h1>Login</h1>

  <label>Email</label>
  <input
    type="email"
    name="email"
    onChange={handleChange}
  />

  <label>Password</label>
  <input
    type="password"
    name="password"
    onChange={handleChange}
  />

  <button onClick={handleLogin}>
    Login
  </button>

  <p>
    Don't have an account?

    <span
      onClick={() => navigate("/signup")}
      style={{
        color: "blue",
        cursor: "pointer",
        marginLeft: "5px"
      }}
    >
      Signup
    </span>

  </p>

</div>


);
}

export default Login;
