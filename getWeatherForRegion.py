import datetime
import pandas as pd
import requests
import json

API_KEY = ""

def getWeatherForecast(cityName):
    baseAddress = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    params = "/next24hours?unitGroup=metric&include=hours%2Cdays&key="
    answerType = "&contentType=json"
    link = baseAddress+cityName+params+API_KEY+answerType
    response = requests.request("GET", link)
    jsonRes = response.json()
    return resultToDF(jsonRes)

def resultToDF(jsonRes):
    baseDF = pd.json_normalize(jsonRes["days"])
    baseDF = baseDF.copy().add_prefix('day_')
    explodedDF = baseDF.explode("day_hours")
    dailyDF = explodedDF["day_hours"].apply(pd.Series)
    dailyDFFormated = dailyDF.copy().add_prefix('hour_')
    mergedDF = pd.concat([baseDF, dailyDFFormated], axis=1)
    columnsToLeave = ['day_tempmax', 'day_tempmin', 'day_temp', 'day_dew', 'day_humidity',
       'day_precip', 'day_precipcover', 'day_solarradiation',
       'day_solarenergy', 'day_uvindex', 'day_moonphase', 'hour_datetimeEpoch',
       'hour_temp', 'hour_humidity', 'hour_dew', 'hour_precip',
       'hour_precipprob', 'hour_snow', 'hour_snowdepth', 'hour_windgust',
       'hour_windspeed', 'hour_winddir', 'hour_pressure', 'hour_visibility',
       'hour_cloudcover', 'hour_solarradiation', 'hour_solarenergy',
       'hour_uvindex', 'hour_severerisk', 'day_datetime']
    mergedDF = mergedDF[columnsToLeave]
    return mergedDF


#print(getWeatherForecast("Kyiv").columns)
