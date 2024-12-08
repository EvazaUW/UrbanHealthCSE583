import React, {useEffect, useState} from "react";
import { Layout, message, Menu, theme, Row, Col } from "antd";
import {getCensusTractAnalysis} from "../utils";
import { useParams } from "react-router-dom";
const { Header } = Layout;

const Dashboard = () => {
  const {geoId} = useParams(); // add this to fetch backend data properly
  const [censusData, setCensusData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    // Fetch data when the component mounts
    const fetchData = async () => {
      try {
        const data = await getCensusTractAnalysis(geoId); // Call fetch function
        console.log("geoid:", geoId)
        setCensusData(data); // Save data to state
        setLoading(false);
      } catch (err) {
        console.log("geoid:", geoId)
        console.error(err);
        // setError("Failed to fetch census tract data");
        setLoading(false);
      }
    };

    fetchData();
  }, [geoId]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

// Ensure censusData exists before accessing its properties
  if (!censusData) return <p>No data available</p>;

// Access specific fields from the fetched data
  const lifeExpectancy = censusData?.lifeexp || "N/A";
  const improvelifeExpectancy = censusData?.improved_urban_indicator_info["Life Expectancy"][0] || "N/A";
  const improved_life_exp_level = censusData?.improved_life_exp_level || "N/A";
  const life_exp_level = censusData?.life_exp_level || "N/A";
  const economicDiversity = censusData?.improved_urban_indicator_info["Ave Economic Diversity"][0] || "N/A";
  const walkabilityIndex = censusData?.improved_urban_indicator_info["Walkability Index"][0] || "N/A";
  const title = censusData?.title || "Census Tract";
  const AveEconomicDiversity = censusData?.current_urban_indicator_info["Ave Economic Diversity"][0] || "N/A";

  return (
    <div style={{ padding: "0", fontFamily: "Arial, sans-serif" }}>
      {/* Top Section */}
      <div
        style={{
          backgroundColor: "#f0f2f7",
          padding: "20px",
          borderRadius: "0",
          boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
          marginBottom: "5px",
          width: "100vw",
          height: "16vh",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "flex-start",
            marginBottom: "15px",
          }}
        >
          {/* Big Title */}
          <h1
            style={{
              fontSize: "32px",
              fontWeight: "bold",
              flex: "1",
              marginRight: "15px",
            }}
          >
            Census Tract Analysis
          </h1>

          <div
            style={{
              flex: "3",
              display: "grid",
              gridTemplateColumns: "100px auto",
              rowGap: "10px",
            }}
          >
          {/* Current Values */}
          <div style={{ display: "flex", alignItems: "center" }}>
            <div style={{ fontSize: "14px", width: "80px" }}>Current Values</div>
          </div>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(8, 1fr)",
              gap: "12px",
            }}
          >
            {Object.entries(censusData.current_urban_indicator_info)
              .filter(([key]) => key !== "Life Expectancy") // Exclude Life Expectancy
              .map(([key, value], index) => {
                // Define shortcut names for each indicator
                const shortcutNames = {
                  "Ave Economic Diversity": "Economic Diversity",
                  "Ave Percent People Employed": "Employment",
                  "Ave Percent People With Health Insurance": "Health Insurance",
                  "Ave Physical Activity": "Physical Activity",
                  "Ave Population Density": "Population Density",
                  "Ave Road Network Density": "Road Network",
                  "Average Distance to Transit": "Transit Distance",
                  "Walkability Index": "Walkability",
                };

                // Use shortcut name or fallback to the original key
                const displayName = shortcutNames[key] || key;

                return (
                  <div
                    key={`current-${index}`}
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      alignItems: "flex-start",
                      position: "relative",
                      width: "130px", // Fixed box width
                    }}
                  >
                    {/* Label with Shortcut Name */}
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        marginBottom: "5px",
                        justifyContent: "space-between",
                        width: "100%",
                      }}
                    >
                      <span
                        style={{
                          fontSize: "12px", // Consistent font size for all names
                        }}
                        title={key} // Full name on hover
                      >
                        {displayName}
                      </span>
                      <button
                        style={{
                          marginLeft: "auto",
                          width: "16px",
                          height: "16px",
                          borderRadius: "50%",
                          border: "none",
                          backgroundColor: "#d9d9d9",
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          cursor: "pointer",
                        }}
                        title={`Info about ${key}`}
                      >
                        <span
                          style={{
                            fontSize: "10px",
                            fontWeight: "light",
                            color: "#555",
                          }}
                        >
                          i
                        </span>
                      </button>
                    </div>

                    {/* Indicator Value */}
                    <div
                      style={{
                        height: "25px",
                        backgroundColor: "#e0e0e0",
                        borderRadius: "4px",
                        width: "100%",
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                        fontSize: "12px",
                        fontWeight: "bold",
                      }}
                    >
                      {value[0]} {/* Display the first value */}
                    </div>
                  </div>
                );
              })
              .slice(0, 8)} {/* Limit to 8 indicators */}
          </div>

          {/* Suggested Values */}
          <div style={{ display: "flex", alignItems: "center" }}>
            <div style={{ fontSize: "14px", width: "80px" }}>Suggested Values</div>
          </div>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(8, 1fr)",
              gap: "12px",
            }}
          >
            {Object.entries(censusData.improved_urban_indicator_info)
              .filter(([key]) => key !== "Life Expectancy") // Exclude Life Expectancy
              .map(([key, value], index) => {
                // Define shortcut names for each indicator
                const shortcutNames = {
                  "Ave Economic Diversity": "Economic Diversity",
                  "Ave Percent People Employed": "Employment",
                  "Ave Percent People With Health Insurance": "Health Insurance",
                  "Ave Physical Activity": "Physical Activity",
                  "Ave Population Density": "Population Density",
                  "Ave Road Network Density": "Road Network",
                  "Average Distance to Transit": "Transit Distance",
                  "Walkability Index": "Walkability",
                };

                // Use shortcut name or fallback to the original key
                const displayName = shortcutNames[key] || key;

                return (
                  <div
                    key={`suggested-${index}`}
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      alignItems: "flex-start",
                      position: "relative",
                      width: "130px", // Fixed box width
                    }}
                  >
                    {/* Label with Shortcut Name */}
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        marginBottom: "5px",
                        justifyContent: "left", // Center align label
                        width: "100%",
                      }}
                    >
                      <span
                        style={{
                          fontSize: "12px", // Consistent font size for all names
                        }}
                        title={key} // Full name on hover
                      >
                        {displayName}
                      </span>
                    </div>

                    {/* Indicator Value */}
                    <div
                      style={{
                        height: "25px",
                        backgroundColor: "#e0e0e0",
                        borderRadius: "4px",
                        width: "100%",
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                        fontSize: "12px",
                        fontWeight: "bold",
                      }}
                    >
                      {value[0]} {/* Display the first value */}
                    </div>
                  </div>
                );
              })
              .slice(0, 8)} {/* Limit to 8 indicators */}
          </div>
         </div> 
        </div>
      </div>

      {/* Main Content Section */}
      <div style={{ padding: "10px", display: "flex", gap: "8px" }}>
        {/* Geography Map Placeholder */}
        <div
          style={{
            backgroundColor: "#e0e0e0",
            height: "80vh",
            width: "46vw",
            borderRadius: "8px",
            boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
          }}
        >
          <p
            style={{
              textAlign: "center",
              lineHeight: "650px",
              fontSize: "18px",
              color: "#555",
              margin: 0,
            }}
          >
            Geography Map Placeholder
          </p>
        </div>

        {/* Column Chart Section */}
        <div
          style={{
            backgroundColor: "#e0e0e0",
            height: "80vh",
            width: "20vw",
            borderRadius: "8px",
            boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
            padding: "15px",
          }}
        >
          <p
            style={{
              textAlign: "center",
              lineHeight: "650px",
              fontSize: "18px",
              color: "#555",
              margin: 0,
            }}
          >
            Column Chart Placeholder
          </p>
        </div>

        {/* Improved and Current Life Expectancy */}
        <div
          style={{
            flex: "1",
            display: "grid",
            gridTemplateRows: "repeat(3, 1fr)",
            gap: "8px",
            width: "30vw",
            height: "80vh",
          }}
        >
          {/* Improved Life Expectancy */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 2fr",
              gap: "8px",
            }}
          >
            {/* Square Box */}
            <div
              style={{
                backgroundColor: "#f0f0f0",
                borderRadius: "8px",
                boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
                padding: "15px",
                height: "100%",
              }}
            >
              <div style={{ fontSize: "48px", fontWeight: "bold" }}>{improvelifeExpectancy}</div>
              <div style={{ fontSize: "18px", color: "#555" }}>YEARS</div>
            </div>

            {/* Rectangle Box */}
            <div
              style={{
                backgroundColor: "#f0f0f0",
                borderRadius: "8px",
                boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                padding: "15px",
              }}
            >
              <div
                style={{
                  fontSize: "43px",
                  fontWeight: "bold",
                  color: "#4CAF50",
                }}
              >
                {improved_life_exp_level}
              </div>
            </div>
          </div>

          {/* Current Life Expectancy */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "2fr 1fr",
              gap: "8px",
            }}
          >
            {/* Rectangle Box */}
            <div
              style={{
                backgroundColor: "#f0f0f0",
                borderRadius: "8px",
                boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                padding: "15px",
              }}
            >
              <div
                style={{
                  fontSize: "43px",
                  fontWeight: "bold",
                  color: "#FF9800",
                }}
              >
                {life_exp_level}
              </div>
            </div>

            {/* Square Box */}
            <div
              style={{
                backgroundColor: "#f0f0f0",
                borderRadius: "8px",
                boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
                padding: "15px",
                height: "100%",
              }}
            >
              <div style={{ fontSize: "48px", fontWeight: "bold" }}>{lifeExpectancy}</div>
              <div style={{ fontSize: "18px", color: "#555" }}>YEARS</div>
            </div>
          </div>

          {/* Rectangle Graph Placeholder */}
          <div
            style={{
              backgroundColor: "#e0e0e0",
              borderRadius: "8px",
              boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
              height: "100%",
              width: "100%", // Full-width to fit available space
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <p style={{ fontSize: "18px", color: "#555" }}>Graph Placeholder</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
