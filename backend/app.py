
from flask import Flask, request, render_template
import geopandas as gpd
import folium as fl
import pandas as pd
import data_preprocessing as dp  # Import pre-processing functions
import os


app = Flask(__name__)

# File paths - changed to relative paths
SHAPEFILE_PATH = "Dataset/Census_Tract_Boundariy_Update/CT10_MetroAll.shp"
CSV_PATH = "Dataset/UpdateMetropolitanCensusTractsData.csv"

# Load data globally to avoid reloading
gdf = gpd.read_file(SHAPEFILE_PATH)
csv_data = pd.read_csv(CSV_PATH)

# csv_data['FGEOIDCT10'] = csv_data['FGEOIDCT10'].astype(str).str.zfill(11)

# Pre-process the data
csv_data['metro'] = csv_data['City'].astype('category')

# Use pre-processing function
processed_csv_data = dp.metro_data_preprocessing(csv_data)
# dp.calculate_percentile_ranks(csv_data)  

merged_gdf = gdf.merge(csv_data, left_on='GEOID10', right_on='FGEOIDCT10')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/map', methods=['POST'])
def generate_map():
    city_name = request.form.get('city_name', '')

    if 'City_x' in merged_gdf.columns:
        city_gdf = merged_gdf[merged_gdf['City_x'].str.contains(city_name, case=False, na=False)]

        if city_gdf.empty:
            return f"<h1>No data found for city: {city_name}. Please check the city name.</h1>"

        city_center = [
            city_gdf.geometry.centroid.y.mean(), 
            city_gdf.geometry.centroid.x.mean()
        ]

        m = fl.Map(location=city_center, zoom_start=10)

        columns_to_map = {
            "Life Expectancy": "YlGnBu",
            "Average Distance to Transit": "PuRd",
            "Ave Economic Diversity": "BuPu",
            "Ave Road Network Density": "OrRd",
            "Walkability Index": "YlOrBr",
            "Ave Percent People Without Health Insurance": "Greens",
            "Ave Population Density": "Purples",
            "Ave Percent People Unemployed": "Reds",
            "Ave Physical Inactivity": "Blues"
        }

        for column, color_scheme in columns_to_map.items():
            fl.Choropleth(
                geo_data=city_gdf,
                data=city_gdf,
                columns=['TRACTCE10', column],
                key_on='feature.properties.TRACTCE10',
                fill_color=color_scheme,
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name=column,
                name=column
            ).add_to(m)

        fl.LayerControl().add_to(m)

        city_path = city_name.replace(" ", "_")
        m.save(f"static/{city_path}_flask.html")

        return render_template('map.html', city_path=city_path)
    return "GeoDataFrame does not contain a city name column."

if __name__ == '__main__':
    app.run(debug=True)