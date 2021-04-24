#################################################
# Tornadoes - Project 2
#################################################

# Dependencies

from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import MongoClient
import pandas as pd

# From data_cleaning file
import data_cleaning

#################################################
# Flask Setup
#################################################

app = Flask(__name__)
CORS(app)

#################################################
# Database Setup
#################################################

conn = "mongodb://localhost:27017"
client = MongoClient(conn)

#################################################
# Flask Routes
#################################################

# loads data from file into mongo db and returns geojson
@app.route("/api/mongo")
def mongo_data():
    db = client.geoDB 
    collection = db.geojson

    features = pd.read_json('data/data.json')["features"].to_list()

    for feature in features:
        collection.insert_one(feature)

    data = db.geojson.find()
    geo = {
    "type":"FeatureCollection",
        "features": []
    }
    for d in data:
        geo["features"].append({
            "type": d["type"],
            "geometry": d["geometry"],
            "properties": d["properties"]
        })
    return geo

# reads data from csv and returns top 10 states by causalty
@app.route("/api/top10")
def top10():
    top10 = {}
    top10 = data_cleaning.top10()
    return top10

# reads data from csv and returns month_year totals for financial loss
@app.route("/api/date_loss")
def date_loss():
    date_loss = {}
    date_loss = data_cleaning.date_loss()
    return date_loss

# To run applicaton

if __name__ == "__main__":
    app.run(debug=False)