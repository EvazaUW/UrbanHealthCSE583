import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { CitySelect, StateSelect } from "react-country-state-city";
import CircularProgress from "@mui/material/CircularProgress";
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
// import bgImage from './img/LandingBackground.png';

function LandingPage({ onCityChange }) {
  const navigate = useNavigate();
  const [selectedCity, setSelectedCity] = useState("");
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const cityOptions = [
    "Seattle",
    "New York",
    "Los Angeles",
    "Chicago",
    "San Francisco",
    "Houston",
    "Phoenix",
    "Boston",
    "Washington DC",
    "Jacksonville",
  ];

  const handleCitySelect = async () => {
    if (selectedCity) {
      setLoading(true); // Start loading
      try {
        const response = await fetch(`http://localhost:5000/map`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ cityName: selectedCity }),
        });
        if (response.ok) {
          navigate(`/city/${selectedCity}`);
        } else {
          console.error("Failed to post city name or fetch city data");
        }
      } catch (error) {
        console.error("Error:", error);
      } finally {
        setLoading(false); // End loading
      }
    }
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
          backgroundImage: `url('https://globalmaps.org/wp-content/uploads/2023/10/World-Map-white-1536x878.png')`, // ${bgImage}
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <Typography
          variant="h2"
          sx={{
            color: "white",
            textShadow: "2px 2px 4px rgba(0, 0, 0, 0.7)",
            marginBottom: 4,
          }}
        >
          Urban Health Environment Consultant
        </Typography>
        <Box
          sx={{
            display: "flex",
            gap: 2,
            flexWrap: "wrap",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <Button
            variant="contained"
            color="primary"
            onClick={() => setDropdownOpen(!dropdownOpen)}
            sx={{
              fontWeight: "bold",
              padding: "10px 20px",
            }}
          >
            Select City
          </Button>
          <FormControl
            sx={{
              display: dropdownOpen ? "block" : "none",
              minWidth: 200,
              width: "200px",
            }}
          >
            <InputLabel>City</InputLabel>
            <Select
              value={selectedCity}
              onChange={(e) => setSelectedCity(e.target.value)}
              sx={{
                width: "90%", // Match FormControl width
                height: "45px", // Set dropdown height
                lineHeight: "45px", // Center text vertically
                fontSize: "16px", // Optional: Adjust font size
              }}
            >
              {cityOptions.map((city) => (
                <MenuItem key={city} value={city}>
                  {city}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <Button
            variant="contained"
            color=""
            onClick={handleCitySelect}
            disabled={!selectedCity}
            sx={{
              fontWeight: "bold",
              padding: "10px 20px",
            }}
          >
            Analyze City
          </Button>
        </Box>
        {loading && (
          <div style={{ textAlign: "center", marginTop: "20px" }}>
            <CircularProgress />
            <p>
              Generating map for {selectedCity}, this takes 5s, please wait...
            </p>
          </div>
        )}
      </Box>
    </div>
  );
}

export default LandingPage;
