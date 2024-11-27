import React from "react";
import { Layout, message, Menu, theme, Row, Col } from "antd";
const { Header } = Layout;

const Dashboard = () => {
  return (
    <div style={{ padding: "0", fontFamily: "Arial, sans-serif" }}>
      {/* Top Section */}
      <div
        style={{
          backgroundColor: "#f0f2f7",
          padding: "20px",
          borderRadius: "0",
          boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
          marginBottom: "15px",
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
              <div style={{ fontSize: "14px", width: "80px" }}>
                Current Values
              </div>
            </div>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(8, 1fr)",
                gap: "6px",
              }}
            >
              {Array.from({ length: 8 }).map((_, index) => (
                <div
                  key={`current-${index}`}
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "flex-start",
                    gap: "3px",
                  }}
                >
                  <div style={{ fontSize: "12px" }}>Indicator {index + 1}</div>
                  <div
                    style={{
                      height: "25px",
                      backgroundColor: "#e0e0e0",
                      borderRadius: "4px",
                      width: "100%",
                    }}
                  />
                </div>
              ))}
            </div>

            {/* Suggested Values */}
            <div style={{ display: "flex", alignItems: "center" }}>
              <div style={{ fontSize: "14px", width: "80px" }}>
                Suggested Values
              </div>
            </div>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(8, 1fr)",
                gap: "6px",
              }}
            >
              {Array.from({ length: 8 }).map((_, index) => (
                <div
                  key={`suggested-${index}`}
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "flex-start",
                    gap: "3px",
                  }}
                >
                  <div style={{ fontSize: "12px" }}>Indicator {index + 1}</div>
                  <div
                    style={{
                      height: "25px",
                      backgroundColor: "#e0e0e0",
                      borderRadius: "4px",
                      width: "100%",
                    }}
                  />
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Section */}
      <div style={{ display: "flex", gap: "8px" }}>
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
            height: "80vh", // Matches the map placeholder height
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
              <div style={{ fontSize: "48px", fontWeight: "bold" }}>85</div>
              <div style={{ fontSize: "18px", color: "#4CAF50" }}>YEARS</div>
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
                  fontSize: "32px",
                  fontWeight: "bold",
                  color: "#4CAF50",
                }}
              >
                EXCELLENT
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
                  fontSize: "32px",
                  fontWeight: "bold",
                  color: "#FF9800",
                }}
              >
                FAIR
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
              <div style={{ fontSize: "48px", fontWeight: "bold" }}>78</div>
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
