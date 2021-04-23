#################################################
# Tornados - Project 2
#################################################

# Dependencies

from flask import Flask, render_template, jsonify, redirect, request
from flask_pymongo import PyMongo
from flask_cors import CORS
import json
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

# mongo = PyMongo(app, uri="mongodb://localhost:27017/geojson")
conn = "mongodb://localhost:27017"
client = MongoClient(conn)

#################################################
# Flask Routes
#################################################

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
    
    print (geo)
    return geo

@app.route("/api/top10")
def top10():
    top10 = {}
    top10 = data_cleaning.top10()
    print(top10)
    return top10

# To run applicaton

if __name__ == "__main__":
    app.run(debug=True)
