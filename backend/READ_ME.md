


---

# Urban Health Backend Project Structure

```plaintext
UrbanHealthProject/
│
├── app.py                     # Main Flask application
├── templates/                 # HTML templates for the Flask app
│   ├── index.html             # Home page with a form to select a city
│   ├── map.html               # Page to display the generated map
│
├── static/                    # Folder for static files (e.g., maps, images)
│   ├── <city_name>_flask.html # Generated maps for cities
│
├── data_preprocessing.py      # Script containing data pre-processing functions
├── Updated_Shape_files/       # Folder for shapefiles
│   └── CT10_MetroAll.shp      # Shapefile with city data
│
├── UpdateMetropolitanCensusTractsData.csv # CSV data for census tracts
