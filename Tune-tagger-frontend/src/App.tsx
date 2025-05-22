import "./App.css";
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "./components/Home";
import Results from "./components/Results";
import Processing from "./components/Processing"

const App: React.FC = () => {

  return (
    <Router basename="/index.html">
      <Routes>
        <Route path="/" element={<Home />} />
        {/* <Route path="/" element={<Processing />} /> */}
        <Route path="/results" element={<Results />} />
        <Route path="/processing" element={<Processing />} />
      </Routes>
    </Router>
  );
};

export default App;
