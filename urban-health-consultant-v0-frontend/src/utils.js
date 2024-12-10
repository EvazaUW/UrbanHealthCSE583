const SERVER_ORIGIN = "";

const getCityAnalysisUrl = `${SERVER_ORIGIN}/city/`;

export const getCityAnalysis = (cityName) => {
  return fetch(`${getCityAnalysisUrl}${cityName}`).then((response) => {
    if (response.status !== 200) {
      throw Error("Failed to get the city analysis data");
    }
    return response.json();
  });
};

const getCensusTractAnalysisUrl = `${SERVER_ORIGIN}/censustract/`;

export const getCensusTractAnalysis = (geoid) => {
  return fetch(`${getCensusTractAnalysisUrl}${geoid}`).then((response) => {
    if (response.status !== 200) {
      throw Error("Failed to get the census tract analysis data 1");
    }
    return response.json();
  });
};
