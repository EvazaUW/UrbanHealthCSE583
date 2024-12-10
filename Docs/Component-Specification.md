## Software components
High level description of the software components.

### Data storage and pre-processing
1. A database that stores the census level data that can be imported into scripts
2. A machine learning model that uses urban indicators to predict life expectancy
    - Inputs: dataframe containing urban indicators and life expectancy
    - Output: trained ML model
3. Custom-defined data processing functions

### Data analysis and visualization
4. Interactive map to display the shaded census tract shapes on top of a street map
    - Technologies: Geopandas, Folium
    - Inputs: Shape files from the census database, census tract level attributes values
    - Outputs: interactive map that displays the shaded census tract shapes on top of a street map, color-coded layers corresponding to values of different urban indicators

5. Statistical plots, including a histogram showing the distribution of life expectancy in the city
    - Technologies: Pandas, Matplotlib, Seaborn
    - Inputs: User selected metropolitan area
    - Output: Histogram

### UI design
6. Landing page with a down menu that allows the user to select a metropolitan area
7. Metropolitan (city)-level webpage
     7.1 Interactive map
     7.2 A display panel that shows the city-level data
     
8. Census tract level webpage
     8.1 A display panel that pops up to display the life expectancy, percentile, and urban indicator values when a census tract is selected
     8.2 Slide bars that allows users to change values of the urban indicator values
     8.3 A display panel that display the “predicted” life expectancy when urban indicator values are changed


## Interactions to accomplish use cases

For the use case of "zooming in on a certain census tract that they are interested in to look at the latest values of the urban health indicators", the user can click on one of the census tracts in the interactive map (component 4) and be directed to the web page for the census tract (component 8). The webpage will contain information on the current values of the 8 urban indicators and life expectancy, which will be populated using the census tract level data (component 1), as well as the percentile in the distribution, which will be calculated using the custom-defined functions (component 3).

## Preliminary plan (in the order of priority)
- Clean and prepare the data
- Exploratory data analysis
- Write functions for data precessing
- Build interactive map
- Build backend
- Build frontend
- Front end back end integration