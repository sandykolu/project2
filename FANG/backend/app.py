from flask import Flask, jsonify

import pandas as pd
from flask_cors import CORS 

df = pd.read_csv("acquisitions.csv")

app = Flask(__name__)
CORS(app)




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