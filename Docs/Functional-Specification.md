## Background 
Urban health indicators are metrics that help assess and monitor the health and quality of life of people in urban areas. They cover a wide range of topics, including indicators that are health *determinants*, which include environmental, socioeconomic and health infrastructure factors that can influence population health, and indicators that represent health *outcomes*, such as life expectancy. 

Multiple health indicators can be aggregated to generate one single urban health index [WHO Guide](https://iris.who.int/bitstream/handle/10665/136839/9789241507806_eng.pdf). The selection of indices and methods of aggregation are driven by the research goal and intended use. Based on prior knowledge in this subject area, we selected the following 8 indicators - transportation accessibility, population density, street network density, unemployment density, health insurance coverage, economic diversity, walkability, and physical inactivity, which can be meaningfully aggregated to reflect the overall urban design infrastructure that influence health of the residents. **Life expectancy is our primary outcome** as it reflects the overall health status in a population. We will use census tract as our unit of analysis. 

Although there are tools to visualize and analyze each indicator, no tool has been built to examine the aggregated effect of these specific indicators on life expectancy. Furthermore, no tool has been built to visualize how changes in one or more indicators can affect life expectancy on the census tract level. For this project, we will first train a regression model to aggregate these indicators, and build an interactive tool that can visualize the impact (derived from the trained model) of these indicators on life expectancy in each census tract in 10 US metropolitan areas.  

## User profile
Our intended users are local policy makers and invested individuals who are interested in learning about their city and neighborhood’s overall health status (life expectancy) and how it is influenced by certain urban indicators. The intended users are expected to have some intuition on what each urban indicator represents but may not understand the details of how each indicator is collected. They likely are not experts in computing but can browse the web with minimal instruction. They want the web interface to be clear and easy to follow, with adequate explanation when it comes to domain specific knowledge. 

## Data sources.
The urban indicators and life expectancy for each census tract are publicly available and downloaded from xxxxx. For each metropolitan area and indicator, there is a tabular data file with the fields xxxx

The shapefile of each census tract is downloaded from xxx

## Use cases
### Use case 1: 
A city-level policy maker may want to get an overview of the life expectancy across each census tract in its jurisdiction. They want to quickly grasp what the life expectancy is like for each geographical region in the city so they can better understand the geographical health disparities in the city. In addition, they may want to know the census tracts that have the poorest life expectancy. The expected interaction between this user will be:
- Input: user selects 1 out the 10 metropolitan areas
- Output: the webpage displays a choropleth map containing the census tracts in this metropolitan area, shaded according to the life expectancy, and a list of the 5 census tracts that have the lowest life expectancy.

### Use case 2: 
The policy maker may want to zoom in on a certain census tract that they are interested in and look at the latest values of the urban health indicators.  
- Input: user select a census tract from the choropleth map by clicking the shape of the census tract
- Output: a panel displaying the life expectancy in the census tract, its percentile in the distribution of life expectancy across all census tracts, and values of the urban indicator measurements. 

### Use case 3: 
A local policy maker or a policy researcher may be interested in which urban indicators influence life expectancy the most and want to see how future policy changes would influence life expectancy. 
- Input: slide bar to change the “future” urban indicators
- Output: the predicted change in life expectancy in a given census tract when one or more areas of the urban infrastructure changes.