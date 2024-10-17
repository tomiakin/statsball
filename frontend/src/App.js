import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Players from "./components/Players";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<h1>Welcome to the Football API</h1>} />
        <Route path="/players" element={<Players />} />
      </Routes>
    </Router>
  );
}

export default App;
