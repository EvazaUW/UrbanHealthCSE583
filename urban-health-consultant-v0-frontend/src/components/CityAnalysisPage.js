import { getCityAnalysis } from "../utils";
import React, { useState, useEffect, useRef } from "react";
import { Layout, message, Menu, theme, Row, Col } from "antd";

const { Header, Content } = Layout;

function CityAnalysisPage() {
  // const .....
  const colSstyle = {
    background: "#ffffff",
    padding: "0px 0",
    height: 24,
    color: "#5c667e",
    textAlign: "center",
  };

  const headerStyle = {
    textAlign: "center",
    fontFamily: "Arial, sans-serif",
    color: "#fff",
    height: "16vh",
    paddingInline: 24,
    lineHeight: "24px",
    backgroundColor: "#f0f2f7", // cdd9e1  0b1947
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
    lineHeight: "16px",
  };

  //   const {
  //     token: { colorBgContainer, borderRadiusLG },
  //   } = theme.useToken();

  return (
    <Layout>
      <Header style={headerStyle}>
        {/* Title */}
        <div style={{ width: "360px" }}>
          <h1
            style={{
              fontSize: "32px",
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
              fontSize: "20px",
              marginLeft: "4vw",
              marginRight: "20px",
              textAlign: "left",
            }}
          >
            Seattle Area
          </h2>
        </div>

        <div
          style={{
            width: "15vw",
            marginTop: "5vh",
            marginRight: "15px",
          }}
        >
          <div
            style={{
              paddingTop: "10px",
              paddingLeft: "30px",
              paddingRight: "20px",
              textAlign: "left",
              minHeight: "6.25vh",
              lineHeight: "16px",
              color: "#5c667e",
              backgroundColor: "#ffffff",
            }}
          >
            <h4>Life Expectancy</h4>
            79 yrs&emsp;&emsp;&emsp;&emsp;Rank: 58.90%
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
              <div style={colSstyle}>col-1</div>
            </Col>
            <Col className="gutter-row" span={6}>
              <div style={colSstyle}>col-2</div>
            </Col>
            <Col className="gutter-row" span={6}>
              <div style={colSstyle}>col-3</div>
            </Col>
            <Col className="gutter-row" span={6}>
              <div style={colSstyle}>col-4</div>
            </Col>
          </Row>
          <div style={{ height: "1vh" }}></div>
          <Row justify="end" gutter={8}>
            <Col className="gutter-row" span={6}>
              <div style={colSstyle}>col-5</div>
            </Col>
            <Col className="gutter-row" span={6}>
              <div style={colSstyle}>col-6</div>
            </Col>
            <Col className="gutter-row" span={6}>
              <div style={colSstyle}>col-7</div>
            </Col>
            <Col className="gutter-row" span={6}>
              <div style={colSstyle}>col-8</div>
            </Col>
          </Row>
        </div>
      </Header>
      <Content>
        <div style={contentStyle}>
          {/* Floating Side Box */}
          <div
            style={{
              position: "relative", // Position relative to the parent container
              top: "100px", // Distance from the top of the container
              left: "60px", // Distance from the left of the container
              width: "18vw", // Width of the box
              padding: "20px", // Padding inside the box
              backgroundColor: "white", // Background color
              borderRadius: "10px", // Rounded corners
              lineHeight: "18px",
              boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)", // Shadow for the floating effect
              zIndex: 999, // Ensures it appears above the map
            }}
          >
            <h3>Seattle Area Statistics</h3>
            <div
              style={{
                height: "160px",
                textAlign: "center",
                border: "1px solid lightgrey",
                marginBottom: "10px",
              }}
            >
              Distribution Graph
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
                  height: "150px",
                //   marginRight: "20px",
                }}
              >
                <h4 style={lineInSiderStyle}>Life Expectancy Average: 80</h4>
                <h4 style={lineInSiderStyle}>Min: 72</h4>
                <h4 style={lineInSiderStyle}>Mid: 76</h4>
                <h4 style={lineInSiderStyle}>Max: 84</h4>
              </div>
              <div>
                <div style={{ height: "20px" }}></div>
                <h3
                  style={{
                    textAlign: "right",
                    color: "#5c667e",
                    lineHeight: "24px",
                    marginLeft: "20px",
                    // width: "80px",
                  }}
                >
                  Health Level Eval: 3 (0-5)
                </h3>
                <p
                  style={{
                    textAlign: "right",
                    color: "#5c667e",
                    lineHeight: "14px",
                    fontSize: "24px",
                  }}
                >
                  Good
                </p>
              </div>
            </div>
            <p style={lineInSiderStyle}>Poorest 5 Census Tracts:</p>
            <li style={lineInSiderStyle}>GEOID1</li>
            <li style={lineInSiderStyle}>GEOID2</li>
            <li style={lineInSiderStyle}>GEOID3</li>
            <li style={lineInSiderStyle}>GEOID4</li>
            <li style={lineInSiderStyle}>GEOID5</li>
          </div>
          <h2 style={{
            position: "absolute",
            top: "27vh",
            left: "45vw",
            color: "lightgrey"
          }}>City Mapping</h2>
          <div
            style={{
              position: "absolute", // Position relative to the parent container
              bottom: "60px", // Distance from the top of the container
              right: "50px", // Distance from the left of the container
              width: "15vw", // Width of the box
              height: "150px",
              padding: "20px", // Padding inside the box
              backgroundColor: "white", // Background color
              borderRadius: "10px", // Rounded corners
              lineHeight: "18px",
              boxShadow: "0px 4px 6px rgba(0, 0, 0, 0.1)", // Shadow for the floating effect
              zIndex: 999, // Ensures it appears above the map
            }}
          >
            <h3>
                Legend
            </h3>
          </div>
        </div>
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
