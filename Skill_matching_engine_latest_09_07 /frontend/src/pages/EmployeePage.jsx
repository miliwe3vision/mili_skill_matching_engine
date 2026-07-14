import { useNavigate } from "react-router-dom";

function EmployeePage() {

  const navigate = useNavigate();

  const user = JSON.parse(
    localStorage.getItem("user")
  );

  return (

    <div className="container">

      <h1>Employee</h1>

      <div>

        <h3>
          Employee Name : {user?.username}
        </h3>

        <h3>
          Role : {user?.role}
        </h3>

      </div>

      <div>

        <div className="buttonRow">

          <button
            onClick={() => navigate("/skills-form")}
          >
            Skills Form
          </button>

          <button
            onClick={() => navigate("/task-assigned")}
          >
            Task Assign
          </button>

        </div>

      </div>

    </div>

  );

}

export default EmployeePage;