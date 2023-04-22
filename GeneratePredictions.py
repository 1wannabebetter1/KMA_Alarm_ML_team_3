import datetime
import pandas as pd
import pickle
from toolbox import getWeatherForRegion as gw
from toolbox import GetVectorForPrediction as gv
import pytz


REGION_FOLDER = "data/regions/"
REGION_FILE = "regions.csv"

MODEL_FOLDER = "data/model/"
MODEL_FILE = "modelSGD_scaled.pkl"

#REGION_FOLDER = "/Users/anastasia/Desktop/programming python/data/regions/"
#MODEL_FOLDER = "/Users/anastasia/Desktop/programming python/data/model/"

def generateAllRegionPredictions():
    df_regions = pd.read_csv(REGION_FOLDER+REGION_FILE)
    cityNames = df_regions['center_city_en']
    for city in cityNames:
        region_id = df_regions.loc[df_regions['center_city_en'] == city, 'region_id'].values[0]
        time = pd.Timestamp.now().round('60min').to_pydatetime().timestamp()
        if(city == "Sumy"):
            generateRegionPredict("Sumy Oblast", region_id, time).to_csv("predictioninfo/" + city + "/" + str(time) + '.csv', index=False)
        elif(city == "Lviv"):
            generateRegionPredict("L'viv", region_id, time).to_csv("predictioninfo/" + city + "/" + str(time) + '.csv',index=False)
        else:
            generateRegionPredict(city, region_id, time).to_csv("predictioninfo/"+city+"/"+str(time)+'.csv', index=False)
        f = open("predictioninfo/lastHour.txt", "w")
        f.write(str(time))
        f.close()
        f2 = open("predictioninfo/lastUpdate.txt", "w")
        f2.write(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        f2.close()

def generateRegionPredict(city, region_id, time):
    df = gw.getWeatherForecast(city)
    df.insert(loc=len(df.columns) - 1, column='region_id', value=region_id)
    removeOld = df.loc[df['hour_datetimeEpoch'] >= time].sort_values(by=['hour_datetimeEpoch'])
    hours12 = removeOld.head(12)
    daysForVectors = hours12['day_datetime'].unique()
    vectorDF = generateVectorDF(daysForVectors)
    merge = hours12.merge(vectorDF, left_on='day_datetime', right_on='date')
    merge = merge.drop(['day_datetime', 'date'], axis=1)
    merge = merge.fillna(0)
    Epoch = merge['hour_datetimeEpoch']
    scaler = pickle.load(open(f"{MODEL_FOLDER}/scaler.pkl", "rb"))
    merge = pd.DataFrame(scaler.transform(merge), columns=merge.columns)
    model = pickle.load(open(MODEL_FOLDER+MODEL_FILE, "rb"))
    merge.columns = merge.columns.astype(str)
    res = model.predict(merge)
    time = pd.DataFrame({'Time': Epoch, 'alarm': res})
    time['date'] = pd.to_datetime(time['Time'], unit='s')
    time['Time'] = time['date'].dt.tz_localize(pytz.utc).dt.tz_convert('Europe/Kyiv').apply(lambda x: x.replace(tzinfo=None))
    time = time.drop(['date'], axis=1)
    return time



def generateVectorDF(daysForVectors):
    vectorDF = pd.DataFrame()
    for i in daysForVectors:
        previousDate = datetime.datetime.strptime(i, '%Y-%m-%d') - datetime.timedelta(days=1)
        temp = gv.GetVector(previousDate.strftime('%Y-%m-%d'))
        temp.insert(loc=0, column='date', value=[i])
        vectorDF = pd.concat([vectorDF, temp], axis=0)
    return vectorDF

generateAllRegionPredictions()
