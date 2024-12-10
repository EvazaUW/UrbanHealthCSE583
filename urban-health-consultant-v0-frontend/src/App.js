import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./components/LandingPage";
import CityAnalysisPage from "./components/CityAnalysisPage";
import CensusTractAnalysisPage from "./components/CensusTractAnalysisPage";
import React, { useState, useEffect } from "react";
import { Layout } from "antd";

function App() {
  // const [message, setMessage] = useState("");

  // useEffect(() => {
  //   // Fetch the message from the Flask backend
  //   const fetchMessage = async () => {
  //     try {
  //       const response = await fetch("http://localhost:5000/hello"); // Flask server URL
  //       const data = await response.json();
  //       setMessage(data.message); // Update state with the message
  //     } catch (error) {
  //       console.error("Error fetching the message:", error);
  //     }
  //   };

  //   fetchMessage();
  // }, []);

  // return (
  //   <div style={{ textAlign: "center", padding: "50px" }}>
  //     <h1>Message from Flask Backend:</h1>
  //     <p>{message || "Loading..."}</p>
  //   </div>
  // );
  const [city, setCity] = useState({ name: "" });
  const handleCitySelection = (cityName) => {
    setCity({ name: cityName });
    console.log("Selected City Name:", cityName);
  };

  return (
    <div className="App">
      <Router>
        <Routes>
          <Route
            path="/"
            element={<LandingPage onCityChange={handleCitySelection} />}
          />
          <Route path="/city/:cityName" element={<CityAnalysisPage />} />
          <Route
            path="/censustract/:geoId"
            element={<CensusTractAnalysisPage />}
          />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
