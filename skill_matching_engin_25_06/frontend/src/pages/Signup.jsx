import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Signup() {

const navigate = useNavigate();

const [role, setRole] = useState("employee");

const [form, setForm] = useState({
username: "",
email: "",
password: "",
confirmPassword: "",
});

const handleChange = (e) => {
setForm({
...form,
[e.target.name]: e.target.value,
});
};

const handleSignup = async () => {


if (form.password !== form.confirmPassword) {
  alert("Passwords do not match");
  return;
}

try {

  const res = await axios.post(
    "http://127.0.0.1:8000/signup",
    {
      username: form.username,
      email: form.email,
      password: form.password,
      role: role,
    }
  );

  alert("Signup Successful");

  // Save logged-in user
  const user = res.data.data[0];

  localStorage.setItem(
    "user",
    JSON.stringify(user)
  );

  // Employee → Skills Form
  if (role === "employee") {
    navigate("/skills-form");
  }

  // Admin → Admin Page
  else {
    navigate("/admin");
  }

} catch (error) {

  console.log(error.response?.data);

  alert(
    error.response?.data?.detail ||
    "Signup Failed"
  );
}


};

return ( <div className="container">


  <h1>Signup</h1>

  <label>Username</label>
  <input
    name="username"
    onChange={handleChange}
  />

  <br /><br />

  <label>Email</label>
  <input
    type="email"
    name="email"
    onChange={handleChange}
  />

  <br /><br />

  <label>Password</label>
  <input
    type="password"
    name="password"
    onChange={handleChange}
  />

  <br /><br />

  <label>Confirm Password</label>
  <input
    type="password"
    name="confirmPassword"
    onChange={handleChange}
  />

  <br /><br />

  <label>Choose Role</label>

  <select
    value={role}
    onChange={(e) => setRole(e.target.value)}
  >
    <option value="employee">Employee</option>
    <option value="admin">Admin</option>
  </select>

  <br /><br />

  <button onClick={handleSignup}>
    Signup
  </button>

</div>


);
}

export default Signup;
