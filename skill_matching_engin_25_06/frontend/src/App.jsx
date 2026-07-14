import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import EmployeePage from "./pages/EmployeePage";
import AdminPage from "./pages/AdminPage";
import SkillsForm from "./pages/SkillsForm";
import TaskForm from "./pages/TaskForm";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route
          path="/"
          element={<Login />}
        />
//tisha_22/06_start---jyare path/ hoy tyare login page open thase
        <Route
          path="/signup"
          element={<Signup />}
        />
//tisha_22/06_start---jyare path/signup hoy tyare signup page open thase
//tisha_22/06_start---same for all
        <Route
          path="/employee"
          element={<EmployeePage />}
        />

        <Route
          path="/admin"
          element={<AdminPage />}
        />

        <Route
          path="/skills-form"
          element={<SkillsForm />}
        />

        <Route
          path="/task-form"
          element={<TaskForm />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;