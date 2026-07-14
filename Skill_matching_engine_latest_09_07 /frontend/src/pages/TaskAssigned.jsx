// By Drashti
import { useEffect, useState } from "react";
import axios from "axios";

function TaskAssigned() {

  const [data, setData] = useState(null);

  useEffect(() => {

    const fetchAssignment = async () => {

      try {

        const user = JSON.parse(
          localStorage.getItem("user")
        );

        const res = await axios.get(
          `http://127.0.0.1:8000/task-assigned/${user.emp_id}`
        );

        setData(res.data);

      } catch (err) {

        console.log(err);

      }

    };

    fetchAssignment();

  }, []);

  // Loading State
  if (!data) {
  return <h2>Loading...</h2>;
}

if (data.assigned === false) {
  return (
    <div
      
    >
      <div
        style={{
          background: "white",
          padding: "40px",
          borderRadius: "20px",
          textAlign: "center"
        }}
      >
        <h1>No Task Assigned</h1>
        <p>You don't have any task assigned yet.</p>
      </div>
    </div>
  );
}

  // No Task Assigned State
  if (data.message === "No task assigned yet") {
    return (
      <div
        style={{
          minHeight: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background:
            "linear-gradient(to right, #7b1fa2, #d1a3d9)",
        }}
      >
        <div
          style={{
            background: "#fff",
            padding: "50px",
            borderRadius: "20px",
            width: "500px",
            textAlign: "center",
            boxShadow: "0 10px 25px rgba(0,0,0,0.2)",
          }}
        >
          <h1
            style={{
              color: "#7b1fa2",
              marginBottom: "20px",
            }}
          >
            No Task Assigned
          </h1>

          <p
            style={{
              fontSize: "18px",
              color: "#555",
            }}
          >
            You don't have any assigned task yet.
          </p>

          <p
            style={{
              marginTop: "15px",
              color: "#888",
            }}
          >
            Please wait until your administrator assigns a task.
          </p>
        </div>
      </div>
    );
  }

  // Employee Has Task
  return (
    <div
      
    >
      <div
        style={{
          background: "#fff",
          padding: "40px",
          borderRadius: "20px",
          width: "450px",
          textAlign: "center",
        }}
      >
        <h1>{data.employee_name}</h1>

        <p>Task: {data.task_name}</p>

        <h1
          style={{
            fontSize: "60px",
            color: "#7b1fa2",
          }}
        >
          {Number(data.final_score).toFixed(2)}%
        </h1>

        <p>Overall Match Score</p>

        <div style={{ marginTop: "30px" }}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
            }}
          >
            <span>Similarity Score</span>

            <span>
              {Number(data.similarity_score).toFixed(2)}%
            </span>
          </div>

          <div
            style={{
              height: "10px",
              background: "#ddd",
              borderRadius: "10px",
            }}
          >
            <div
              style={{
                width: `${data.similarity_score}%`,
                height: "100%",
                background: "#7b1fa2",
                borderRadius: "10px",
              }}
            />
          </div>
        </div>

        <div style={{ marginTop: "20px" }}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
            }}
          >
            <span>Workload Score</span>

            <span>
              {Number(data.workload_score).toFixed(2)}%
            </span>
          </div>

          <div
            style={{
              height: "10px",
              background: "#ddd",
              borderRadius: "10px",
            }}
          >
            <div
              style={{
                width: `${data.workload_score}%`,
                height: "100%",
                background: "#7b1fa2",
                borderRadius: "10px",
              }}
            />
          </div>
        </div>

      </div>
    </div>
  );
}

export default TaskAssigned;
