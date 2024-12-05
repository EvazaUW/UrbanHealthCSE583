
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
import os.path
import sys
import joblib
from pathlib import Path
from PIL import Image

app = Flask(__name__)

# File paths - changed to relative paths
SHAPEFILE_PATH = "Dataset/Census_Tract_Boundariy_Update/CT10_MetroAll.shp"
CSV_PATH = "Dataset/UpdateMetropolitanCensusTractsData.csv"


# Load data globally to avoid reloading
gdf = gpd.read_file(SHAPEFILE_PATH)
csv_data = pd.read_csv(CSV_PATH)

csv_data['FGEOIDCT10'] = csv_data['FGEOIDCT10'].astype(str).str.zfill(11)

urban_indicators = ['Average Distance to Transit', 'Ave Economic Diversity', 
                        'Ave Road Network Density', 'Walkability Index',
                        'Ave Percent People Without Health Insurance', 'Ave Population Density',
                        'Ave Percent People Unemployed', 'Ave Physical Inactivity']

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
        # placeholder
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

@app.route('/censustract/<geoid>', methods=['GET', 'POST'])
def get_census_tract_analysis(geoid):
    if request.method == 'POST':
        #placeholder for getting slider bar input for generate_indicator_comparison_plot
        pass
    else:
        columns = [
            'FGEOIDCT10',
            'Life Expectancy',
            'Ave Economic Diversity',
            'Ave Physical Activity',
            'Average Distance to Transit',
            'Ave Road Network Density',
            'Walkability Index',
            'Ave Percent People With Health Insurance',
            'Ave Population Density',
            'Ave Percent People Employed',
            'life_exp_pred'
        ]
        features = columns[2:10]
        prepared_df = ct.df_feature_reverse_for_ml(ct.clean_data(csv_data))
        lifeexp = prepared_df[prepared_df['FGEOIDCT10'] == geoid]['Life Expectancy'].iloc[0]

        # # Load the saved model and scaler
        BASE_DIR = Path(__file__).parent
        MODEL_PATH = os.path.join(BASE_DIR, '../Dataset/ml-model/ridge_default.joblib')
        SCALER_PATH = os.path.join(BASE_DIR, '../Dataset/ml-model/std_scaler_ridge_default.bin')
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}, current path is {BASE_DIR}")
        if not os.path.exists(SCALER_PATH):
            raise FileNotFoundError(f"Scaler file not found at {SCALER_PATH}")
        model_default = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)

        # get indicators and life expectancy infos
        features_for_prediction = prepared_df[features]  # Use the same features used for training
        features_for_prediction = scaler.transform(features_for_prediction)
        life_exp_pred = model_default.predict(features_for_prediction)
        prepared_df['life_exp_pred'] = life_exp_pred
        curlifepred = prepared_df[prepared_df['FGEOIDCT10'] == geoid]['life_exp_pred'].iloc[0]
        cur_inds_info_dict, improved_inds_info_dict = ct.get_recommendations(prepared_df, geoid, features)

        # get current and improved life expectancy level evaluation
        life_exp_level = ct.get_ct_life_exp_level(lifeexp)
        improved_life_exp_level = ct.get_improved_ct_life_exp_level(improved_inds_info_dict['Life Expectancy'][0])

        # image generation
        features = columns[2:10]
        city_name = prepared_df[prepared_df['FGEOIDCT10'] == geoid]['City'].iloc[0]
        img_name = f'Feature importance for {city_name}.png'
        IMG_PATH = os.path.join(BASE_DIR, f'../Dataset/imgs_generated/{img_name}')
        img64_list = []
        if os.path.exists(IMG_PATH):
            tract_life_exp_graph = Image.open(IMG_PATH)
            img_io = BytesIO()
            tract_life_exp_graph.save(img_io, format="PNG")  # Save image to buffer in PNG format
            img_bytes = img_io.getvalue()  # Get bytes from the buffer
            img_base64 = base64.b64encode(img_bytes).decode("utf-8")  # Encode to Base64
            img64_list.append(img_base64)
        else:
            tract_life_exp_graph = ct.generate_ct_life_exp_posi_in_city_distribution(prepared_df, geoid)
            img_io = BytesIO()
            tract_life_exp_graph.savefig(img_io, format='PNG')
            img_io.seek(0) 
            plt.close(tract_life_exp_graph)
            img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
            img64_list.append(img_base64)
        recommendation_graph = ct.generate_indicator_comparison_plot(cur_inds_info_dict, improved_inds_info_dict, geoid)
        ind_importance_graph = ct.generate_feature_importance_graph(model_default, features, city_name)
        images = [recommendation_graph, ind_importance_graph]
        for img in images:
            img_io = BytesIO()
            img.savefig(img_io, format='PNG')
            img_io.seek(0) 
            plt.close(img)
            img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
            img64_list.append(img_base64)


        returned_data = {
            "title": f"this is census tract {geoid}",
            "lifeexp": lifeexp,
            "life_exp_level": life_exp_level,
            "life_exp_pred": curlifepred,
            "improved_life_exp_level": improved_life_exp_level,
            "images": {
                "tract_life_exp_graph": img64_list[0],
                "recommendation_graph": img64_list[1],
                "ind_importance_graph": img64_list[2],
            },
            "current urban indicator info": cur_inds_info_dict,
            "improved urban indicator info": improved_inds_info_dict
        }
    
    return jsonify(returned_data)

if __name__ == '__main__':
    app.run(debug=True)

