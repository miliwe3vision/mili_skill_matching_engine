import { useNavigate } from "react-router-dom";

function AdminPage(){

const navigate=useNavigate();

return(

<div className="container">

<h1>Admin</h1>

<div>

<h3>Name :</h3>
<h3>Role : Admin</h3>

</div>

<div className="buttonRow">

<button
onClick={()=>navigate("/task-form")}
>
Task Form
</button>

<button>
Assign Task
</button>

<button>
Employee Details
</button>

</div>

</div>

)

}

export default AdminPage;