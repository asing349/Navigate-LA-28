import React from "react";

function App() {
  return (
    <div style={{ fontFamily: "Arial, sans-serif", textAlign: "center", marginTop: "50px" }}>
      <h1 style={{ color: "navy" }}>Welcome to Your React Frontend</h1>
      <p>Your frontend setup is working correctly!</p>
      <button
        style={{
          padding: "10px 20px",
          fontSize: "16px",
          backgroundColor: "navy",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
        onClick={() => alert("Frontend is functional!")}
      >
        Click Me
      </button>
    </div>
  );
}

export default App;
