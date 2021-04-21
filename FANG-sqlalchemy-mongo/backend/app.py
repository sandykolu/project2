from flask import Flask, jsonify
from flask_pymongo import PyMongo
import pandas as pd
from flask_cors import CORS 
from sqlalchemy import create_engine
engine = create_engine('postgres://postgres:2d9c92d9c9@localhost:5432/project2')




df = pd.read_csv("acquisitions.csv")

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/acquisitionsDB"
mongo = PyMongo(app)

CORS(app)


@app.route("/api/mongo/acquistions")
def acquisition_mongo():

    data = mongo.db.acquisitions.find()
    acquisitions_list = []

    for d in data: 
        acquisitions_list.append( { 
            "AcquisitionID": d["AcquisitionID"],
            'ParentCompany': d["ParentCompany"], 
            "AcquisitionYear": int(d["AcquisitionYear"])
        })
    print(acquisitions_list)
    return jsonify(acquisitions_list)


@app.route("/api/country_count")
def country_count():
    data = engine.execute("SELECT country, count(country) as country_count FROM acquisition GROUP BY country;")
    
    country_list = []
    count_list = []

    for country, count in data.fetchall(): 
        country_list.append(str(country))
        count_list.append(int(count))
    print(country_list)
    print(count_list)
    return jsonify([{
        "x": country_list,
        "y":count_list,
        "type": "bar"
    }])



@app.route("/api/acquistions")
def fang():
    vc = df["ParentCompany"].value_counts()

    print(vc)

    y = []
    for i in list(df["ParentCompany"].value_counts().values):
        y.append(int(i))
    data = [{
        "x": list(vc.index),
        "y": y,
        "type": "bar"
    }]

    print(data)
    
    return jsonify(data)


if __name__ == '__main__':
    app.run()