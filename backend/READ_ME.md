UrbanHealthProject backend structure
│
├── app.py                     # Main Flask application
├── templates/
│   ├── index.html             # Home page with form to select city
│   ├── map.html               # Page to display the map
│
├── static/
│   ├── <city_name>_flask.html # Maps generated dynamically
│
├── data_preprocessing.py      # Contains pre-processing functions
├── Updated_Shape_files/
│   └── CT10_MetroAll.shp      # Shapefile
│
├── UpdateMetropolitanCensusTractsData.csv # CSV data
