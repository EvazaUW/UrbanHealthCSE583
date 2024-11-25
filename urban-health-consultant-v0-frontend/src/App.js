import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./components/LandingPage";
import CityAnalysisPage from "./components/CityAnalysisPage";
import CensusTractAnalysisPage from "./components/CensusTractAnalysisPage";
import React, { useState, useEffect } from "react";
import { Layout } from "antd";

function App() {
  // const [message, setMessage] = useState("");

  // useEffect(() => {
  //   fetch("/hello")
  //     .then((response) => response.json())
  //     .then((data) => setMessage(data.message));
  // }, []);

  // return (
  //   <div>
  //     <h1>{message}</h1>
  //     <h2>Hello from React</h2>
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
