import datetime as dt
from datetime import timedelta
import json

import requests
from flask import Flask, jsonify, request

API_TOKEN = ""

app = Flask(__name__)

def generate_forecast(location: str):
    url = "https://visual-crossing-weather.p.rapidapi.com/forecast"

    querystring = {"aggregateHours":"1",
                   "location":location,
                   "contentType":"json",
                   "unitGroup":"metric",
                   "shortColumnNames":"0"}

    headers = {
        "X-RapidAPI-Key": API_TOKEN,
        "X-RapidAPI-Host": "visual-crossing-weather.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    return json.loads(response.text)

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


@app.route(
    "/forecast/api/v1",
    methods=["POST"],
)
def forecast_endpoint():
    json_data = request.get_json()

    if json_data.get("token") is None:
        raise InvalidUsage("token is required", status_code=400)

    token = json_data.get("token")

    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)

    if json_data.get("location") is None:
        raise InvalidUsage("location is required", status_code=400)

    location = json_data.get("location")

    forecast = generate_forecast(location)
    values = get_forecast(forecast['locations'][location]['values'])
    
    result = {}
    result['values'] = values

    return result

def get_forecast(values):
    d = dt.datetime.now() + timedelta(hours=1)
    date = d.date().isoformat() + 'T' + d.strftime('%H')

    iter = 0
    hours = 12
    forecast_values = [None] * hours
    flag = False

    for value in values:
        
        if date in value['datetimeStr']:
            flag = True

        if flag:
            forecast_values[iter] = value
            iter += 1
            
        if iter >= hours:
            break;
    
    return forecast_values