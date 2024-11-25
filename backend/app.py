from flask import Flask, request, jsonify
from markupsafe import escape
import data_preprocessing as dp
import os

app = Flask(__name__)

@app.route('/hello')
def hello():
   return jsonify({'message': 'Hello from Flask!'})

@app.route('/')
def home():
    return 'This is the home page!'

@app.route('/city/<cityname>', methods=['GET', 'POST'])
def show_city(cityname):
    if request.method == 'POST':
        pass
    else:
        index_means, index_rank_means = dp.get_city_ind_avg(cityname, dp.data)


        return index_means
        

@app.route('/censustract/<geoid>')
def show_census_tract(geoid):
    return f'This page has census tract {geoid} analysis'

if __name__ == '__main__':
    app.run(debug=True)

