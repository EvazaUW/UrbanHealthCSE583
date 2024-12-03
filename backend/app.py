
from flask import Flask, request, jsonify, render_template
import geopandas as gpd
import folium as fl
import pandas as pd
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # Ensure non-GUI backend

# other custom defined modules
import data_preprocessing as dp
import functions_ct as ct


app = Flask(__name__)

# File paths - changed to relative paths
SHAPEFILE_PATH = "Dataset/Census_Tract_Boundariy_Update/CT10_MetroAll.shp"
CSV_PATH = "Dataset/UpdateMetropolitanCensusTractsData.csv"

# Load data globally to avoid reloading
gdf = gpd.read_file(SHAPEFILE_PATH)
csv_data = pd.read_csv(CSV_PATH)

csv_data['FGEOIDCT10'] = csv_data['FGEOIDCT10'].astype(str).str.zfill(11)

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


@app.route('/city/<cityname>', methods=['GET', 'POST'])
def get_city_analysis(cityname):
    if request.method == 'POST':
        pass
    else:
        city_index_means, city_index_rank_means = dp.get_city_ind_avg(cityname, processed_csv_data)
        city_life_exp_mean, city_life_exp_level, city_lowest_tracts= dp.get_city_life_exp(cityname, processed_csv_data)
        
        city_life_exp_img = dp.get_city_life_exp_dist_plot(cityname, processed_csv_data)

        # store the image in a BytesIO object that uses in-memory buffer
        img_io = BytesIO()
        city_life_exp_img.savefig(img_io, format='PNG')
        img_io.seek(0) 
        plt.close(city_life_exp_img)

        # encode the image in base64 string 
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

        returned_data = {
            "city_index_means": city_index_means.to_dict(),
            "city_index_rank_means": city_index_rank_means.to_dict(),
            "city_life_exp_mean": city_life_exp_mean,
            "city_life_exp_level": city_life_exp_level,
            "city_lowest_life_exp_tracts": city_lowest_tracts.to_json(orient = 'records'),
            "image": img_base64
        }

        #### example frontend code to incorporate the image
        # fetch('http://localhost:5000/city/<cityname>')
        #  .then(response => response.json())
        #  .then(data => {
        #    const imgElement = document.getElementById('dynamic-image');
        #    imgElement.src = `data:image/png;base64,${data.image}`;
        # });

        return jsonify(returned_data)

@app.route('/censustract/<geoid>')
def get_census_tract_analysis(geoid):
    return f"This is the page for the census tract analysis"

if __name__ == '__main__':
    app.run(debug=True)

