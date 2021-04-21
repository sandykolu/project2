#################################################
# Tornados - Project 2
#################################################

# Dependencies

from flask import Flask, render_template, jsonify, redirect, request
from flask_pymongo import PyMongo
from flask_cors import CORS

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

mongo = PyMongo(app, uri="mongodb://localhost:27017/Tornados")

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/clean")
def clean():
    geojson = data_cleaning.clean()
    return geojson


# To run applicaton

if __name__ == "__main__":
    app.run(debug=True)
