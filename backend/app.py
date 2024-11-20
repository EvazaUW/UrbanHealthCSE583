from flask import Flask, jsonify
from markupsafe import escape

app = Flask(__name__)

@app.route('/hello')
def hello():
   return jsonify({'message': 'Hello from Flask!'})

@app.route('/')
def home():
    return 'This is the home page!'

@app.route('/city/<cityname>')
def show_city(cityname):
    return f'This page has {escape(cityname)}\'s analysis'

@app.route('/censustract/<geoid>')
def show_census_tract(geoid):
    return f'This page has census tract {geoid} analysis'

if __name__ == '__main__':
    app.run()
