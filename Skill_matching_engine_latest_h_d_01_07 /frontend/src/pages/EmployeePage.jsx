import { useNavigate } from "react-router-dom";

function EmployeePage() {

const navigate = useNavigate();

const employeeData=
JSON.parse(
localStorage.getItem("employeeData")
);

return(

<div className="container">

<h1>Employee</h1>

<div>

<h3>
Employee Name :
{employeeData?.name}
</h3>

<h3>
Role :
{employeeData?.role}
</h3>

</div>

<div>

<div className="buttonRow">

<button
onClick={()=>navigate("/skills-form")}
>
Skills Form
</button>

<button>
Task Assign
</button>

</div>


</div>

</div>

)

}

export default EmployeePage;