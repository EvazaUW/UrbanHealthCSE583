import { getCityAnalysis } from "../utils";
import React, { useState, useEffect, useRef } from "react";
import { useParams } from "react-router-dom";
import { Layout, message, Menu, theme, Row, Col } from "antd";

const { Header, Content } = Layout;

function CityAnalysisPage() {
  // const { cityName } = props;
  const { cityName } = useParams();
  const [cityData, setCityData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [poorestCTs, setPoorestCTs] = useState(null);

  // Fetch data on component mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://localhost:5000/city/${cityName}`); // Flask server URL
        const data = await response.json();
        const parsedData = JSON.parse(data.city_lowest_life_exp_tracts);
        setPoorestCTs(parsedData);
        setCityData(data); // Update state with the message
        setLoading(false);
      } catch (error) {
        console.error("Error fetching the city Data:", error);
        setLoading(false);
      }
    };
    fetchData();
  }, [cityName]);

  // Conditional rendering
  if (loading) {
    return <p>Loading...</p>;
  }
  if (error) {
    return <p>{error}</p>;
  }
  // Access specific fields from the fetched data
  const city_life_exp_mean = cityData.city_life_exp_mean;
  const Eco_diversity_value =
    cityData.city_index_means["Ave Economic Diversity"];
  const Ave_unemployed =
    cityData.city_index_means["Ave Percent People Unemployed"];
  const Ave_without_healthIns =
    cityData.city_index_means["Ave Percent People Without Health Insurance"];
  const Ave_physical_inactivity =
    cityData.city_index_means["Ave Physical Inactivity"];
  const Ave_population_density =
    cityData.city_index_means["Ave Population Density"];
  const Ave_roadnet_density =
    cityData.city_index_means["Ave Road Network Density"];
  const Ave_dist_to_transit =
    cityData.city_index_means["Average Distance to Transit"];
  const Ave_walkability = cityData.city_index_means["Walkability Index"];

  const city_life_exp_level = cityData.city_life_exp_level;
  const city_life_exp_level_num = cityData.city_life_exp_level_num;
  const city_lowest_life_exp_tracts = cityData.city_lowest_life_exp_tracts; // list
  const highest_life_exp = cityData.highest_life_exp;
  const mid_life_exp = cityData.mid_life_exp;
  const title =
    cityName === ("Seattle" || "Washington DC" || "Boston" || "San Francisco")
      ? cityName + " Area"
      : cityName;
  // const imgElement = document.getElementById('dynamic-image');
  // imgElement.src = `cityData:image/png;base64,${cityData.image}`;

  // const .....
  const colSstyle = {
    background: "#ffffff",
    paddingTop: "3px",
    height: "2.7vh",
    color: "#212121",
    textAlign: "left",
    fontSize: "14px",
    paddingInline: "20px",
    borderRadius: "5px",
  };

  const headerStyle = {
    textAlign: "center",
    fontFamily: "Arial, sans-serif",
    color: "#fff",
    height: "16vh",
    paddingInline: 24,
    lineHeight: "24px",
    backgroundColor: "#e7f0f9", // cdd9e1  0b1947  ecf2f8  f0f2f7  e7f0f9
    display: "flex",
    alignItems: "flex-start",
  };

  const contentStyle = {
    textAlign: "center",
    minHeight: "82.3vh",
    lineHeight: "60px",
    color: "#5c667e",
    backgroundColor: "#fbfbfb",
    backgroundImage: `url(https://t4.ftcdn.net/jpg/01/92/49/95/360_F_192499522_CIWxRvKRlBmxaEcsqJjgugqUpBZCJRDM.jpg)`,
    backgroundSize: "cover",
    backgroundPosition: "center",
  };

  const lineInSiderStyle = {
    textAlign: "left",
    color: "#5c667e",
    lineHeight: "18px",
    fontSize: "16px",
  };

  //   const {
  //     token: { colorBgContainer, borderRadiusLG },
  //   } = theme.useToken();

  return (
    <Layout>
      <Header style={headerStyle}>
        {/* Title */}
        <div style={{ width: "22vw" }}>
          <h1
            style={{
              fontSize: "36px",
              fontWeight: "bold",
              flex: "3",
              marginTop: "5vh",
              marginLeft: "4vw",
              marginRight: "20px",
              textAlign: "left",
            }}
          >
            City Analysis
          </h1>
          <h2
            style={{
              fontSize: "24px",
              marginLeft: "4vw",
              marginRight: "20px",
              textAlign: "left",
            }}
          >
            {title}
          </h2>
        </div>

        <div
          style={{
            width: "14vw",
            marginTop: "5vh",
            marginRight: "15px",
          }}
        >
          <div
            style={{
              paddingTop: "15px",
              paddingLeft: "30px",
              paddingRight: "20px",
              textAlign: "left",
              minHeight: "6vh",
              lineHeight: "16px",
              color: "#5c667e",
              backgroundColor: "#ffffff",
              borderRadius: "10px",
              fontSize: "16px",
            }}
          >
            <h4>Life Expectancy</h4>
            {city_life_exp_mean} yrs&emsp;&emsp;Rank: {city_life_exp_level}
          </div>
        </div>

        {/* Grid */}
        <div
          style={{
            width: "60vw",
            marginTop: "5vh",
          }}
        >
          <Row justify="end" gutter={8}>
            <Col className="gutter-row" span={6}>
              <div style={colSstyle}>
                Economic Diversity Score: &emsp;&emsp;&emsp;&emsp;
                {Eco_diversity_value.toFixed(2)}
              </div>
            </Col>
            <Col className="gutter-row" span={6}>
              <div style={colSstyle}>
                Percent People Unemployed Rate: &emsp;
                {Ave_unemployed.toFixed(2)}
              </div>
            </Col>
            <Col className="gutter-row" span={6}>
              <div style={colSstyle}>
                Percent Without Health Insurance: &ensp;&ensp;
                {Ave_without_healthIns.toFixed(2)}
              </div>
            </Col>
            <Col className="gutter-row" span={6}>
              <div style={colSstyle}>
                Physical Inactivity: &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
                {Ave_physical_inactivity.toFixed(2)}
              </div>
            </Col>
          </Row>
          <div style={{ height: "0.6vh" }}></div>
          <Row justify="end" gutter={8}>
            <Col className="gutter-row" span={6}>
              <div style={colSstyle}>
                Population Density: &emsp;&emsp;&emsp;&emsp;&emsp;
                {Ave_population_density.toFixed(2)}
              </div>
            </Col>
            <Col className="gutter-row" span={6}>
              <div style={colSstyle}>
                Road Network Density: &emsp;&emsp;&emsp;&emsp;&emsp;&ensp;
                {Ave_roadnet_density.toFixed(2)}
              </div>
            </Col>
            <Col className="gutter-row" span={6}>
              <div style={colSstyle}>
                Average Distance to Transit: &emsp;&emsp;&ensp;
                {Ave_dist_to_transit.toFixed(2)}
              </div>
            </Col>
            <Col className="gutter-row" span={6}>
              <div style={colSstyle}>
                Walkability Index:
                &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;
                {Ave_walkability.toFixed(2)}
              </div>
            </Col>
          </Row>
        </div>
      </Header>
      <Content>
        {/* <div style={contentStyle}> */}
        <iframe
          src={`http://localhost:5000/static/${cityName.replace(
            " ",
            "_"
          )}_flask.html`}
          title={`${cityName} Map`}
          style={{ width: "100vw", height: "81.7vh", border: "none" }}
        >
          {/* </div> */}
        </iframe>

        {/* Floating Side Box */}
        <div
          style={{
            position: "absolute", // Position relative to the parent container
            top: "32vh", // Distance from the top of the container
            left: "5vw", // Distance from the left of the container
            width: "18vw", // Width of the box
            padding: "20px", // Padding inside the box
            paddingBottom: "30px",
            backgroundColor: "white", // Background color
            borderRadius: "10px", // Rounded corners
            lineHeight: "18px",
            boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)", // Shadow for the floating effect
            zIndex: 999, // Ensures it appears above the map
          }}
        >
          <h3>{cityName} Statistics</h3>
          <div
            style={{
              height: "18vh",
              textAlign: "center",
              border: "1px solid lightgrey",
              marginBottom: "10px",
              borderRadius: "10px", // Optional: Add rounded corners
              display: "flex", // Center the image
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <img
              src={`data:image/png;base64, ${cityData.image}`}
              alt="City Analysis"
              style={{
                width: "100%", // Full width
                height: "100%", // Full height
                objectFit: "contain", // Ensure the image is contained within the box
              }}
            />
          </div>
          <div
            style={{
              display: "flex",
              alignItems: "flex-start",
            }}
          >
            <div
              style={{
                width: "120px",
                height: "13vh",
                //   marginRight: "20px",
              }}
            >
              <h4 style={lineInSiderStyle}>
                Life Expectancy Average: {city_life_exp_mean}
              </h4>
              <h4 style={lineInSiderStyle}>
                Min: {poorestCTs[0]["Life Expectancy"]}
              </h4>
              <h4 style={lineInSiderStyle}>Mid: {mid_life_exp}</h4>
              <h4 style={lineInSiderStyle}>Max: {highest_life_exp}</h4>
            </div>
            <div>
              {/* <div style={{ height: "20px" }}></div> */}
              <h3
                style={{
                  textAlign: "right",
                  color: "#5c667e",
                  lineHeight: "30px",
                  marginLeft: "20px",
                  fontSize: "20px",
                  // width: "80px",
                }}
              >
                Health Level Eval: {city_life_exp_level_num} (1-5)
              </h3>
              <div style={{ height: "10px" }}></div>
              <p
                style={{
                  textAlign: "right",
                  color: "#5c667e",
                  lineHeight: "14px",
                  fontSize: "24px",
                }}
              >
                {city_life_exp_level}
              </p>
            </div>
          </div>
          <p style={lineInSiderStyle}>
            <strong>Poorest 5 Census Tracts:</strong>
          </p>
          {poorestCTs.map((item, index) => (
            <li
              key={index}
              style={{ color: "#3d5d7c", lineHeight: "20px", fontSize: "18px" }}
            >
              GEOID: {item.FGEOIDCT10}, &emsp;Life Exp:&ensp;
              {item["Life Expectancy"]}
            </li>
          ))}
        </div>
        {/* <h2
          style={{
            position: "absolute",
            top: "27vh",
            left: "45vw",
            color: "lightgrey",
          }}
        >
          city anaysis {city_index_rank_means_value}
        </h2> */}
        {/* Floating Layers Info */}
        <div
          style={{
            position: "absolute", // Position relative to the parent container
            bottom: "13.8vh", // Distance from the top of the container
            right: "5vw", // Distance from the left of the container
            width: "5.4vw", // Width of the box
            height: "44px",
            padding: "20px", // Padding inside the box
            paddingLeft: "24px",
            backgroundColor: "white", // Background color
            borderRadius: "10px", // Rounded corners
            lineHeight: "0px",
            fontSize: "18px",
            boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)", // Shadow for the floating effect
            zIndex: 999, // Ensures it appears above the map
          }}
        >
          <h3>Layers</h3>
        </div>
        {/* Footer */}
        <div
          style={{
            backgroundColor: "#f2f2f2",
            height: "1.6vh",
            textAlign: "center",
            fontSize: "10px",
          }}
        >
          Urban Health Consultant ©2024 Created by Eva's Group in CSE 583
        </div>
      </Content>
    </Layout>
  );
}

export default CityAnalysisPage;
