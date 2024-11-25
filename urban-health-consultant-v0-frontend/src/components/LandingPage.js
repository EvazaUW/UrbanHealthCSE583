import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { CitySelect, StateSelect } from "react-country-state-city";
import "react-country-state-city/dist/react-country-state-city.css";
import {
  Box,
  Button,
  TextField,
  MenuItem,
  Typography,
  Select,
  FormControl,
  InputLabel,
} from "@mui/material";

function LandingPage({ onCityChange }) {
  const [state, setState] = useState({ name: "" });
  const [city, setCity] = useState({ name: "" });
  const navigate = useNavigate();
  const handleCityChange = (e) => {
    const selectedCityName = e.name;
    console.log("from landing");
    console.log("Selected City Name:", selectedCityName);
    setCity({ name: selectedCityName });
    onCityChange(selectedCityName);
    navigate(`/city/${selectedCityName}`);
  };
  return (
    <div>
      <Box
        className="landing-page"
        style={{
          height: "100vh",
          width: "100vw",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          backgroundImage: `url('./img/LandingBackground.png')`, // Replace with your background GIF
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <Typography
          variant="h3"
          sx={{
            color: "white",
            textShadow: "2px 2px 4px rgba(0, 0, 0, 0.7)",
            marginBottom: 4,
          }}
        >
          Urban Health Environment Consultant
        </Typography>
        <div style={{ display: "flex", flexDirection: "column" }}>
          <CitySelect
            // countryid={countryid}
            // stateid={state.id}
            // onChange={(e) => console.log(e)}
            onChange={handleCityChange}
            placeHolder="Select City"
            style={{
              cursor: "pointer",
              width: "200px",
              height: "40px",
              fontFamily: "Arial, sans-serif",
              color: "#333",
              fontWeight: "bold",
              backgroundPosition: "right 10px center",
              backgroundSize: "16px",
            }}
          />
        </div>
        <Button onClick={handleCityChange}>Analyze City</Button>
      </Box>
    </div>
  );
}

export default LandingPage;
