import json
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

REGION_FOLDER = "data/regions/"
REGION_FILE = "regions.csv"
PREDICTION_FOLDER = "predictioninfo/"


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def home_page():
    return "<p><h2>Hourly forecast for 12 hours ahead.</h2></p>"


def cityPrediction(location):
    f = open(PREDICTION_FOLDER+'lastHour.txt', "r")
    lastHour = f.read()
    f.close()
    prediction = pd.read_csv(PREDICTION_FOLDER+location+'/'+lastHour+'.csv')
    dict = pd.Series(prediction.alarm.values,index=prediction.Time).to_dict()
    return {location: dict}


@app.route(
    "/forecast/api/v1",
    methods=["POST"],
)
def forecast_endpoint():
    json_data = request.get_json()
    if json_data.get("location") is None:
        raise InvalidUsage("location is required", status_code=400)
    location = json_data.get("location")
    df_regions = pd.read_csv(REGION_FOLDER+REGION_FILE)
    cityNames = df_regions['center_city_en']
    f = open(PREDICTION_FOLDER+'lastUpdate.txt', "r")
    lastUpdate = f.read()
    f.close()
    res = {
        "last_model_train_time" : "17.04.2023 20:04:26",
        "last_prediciotn_time" : lastUpdate
    }
    if(location=="all"):
        for city in cityNames:
            res.update(cityPrediction(city))
    elif(location in cityNames.unique()):
         res.update(cityPrediction(location))
    else:
        raise InvalidUsage("wrong location", status_code=400)
    return json.dumps(res,indent = 4)



