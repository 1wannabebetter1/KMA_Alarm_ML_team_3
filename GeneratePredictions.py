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

#method that generates forecasts for all regions
def generateAllRegionPredictions():
    #open the dataset with regions to extract the names of regional centres in English
    df_regions = pd.read_csv(REGION_FOLDER+REGION_FILE)
    # create an array with the names of regional centres in English
    cityNames = df_regions['center_city_en']
    # for each city from the array, create a forecast
    for city in cityNames:
        #get the number of the corresponding region, because we write the region number to the vector
        region_id = df_regions.loc[df_regions['center_city_en'] == city, 'region_id'].values[0]
        # get the present time to know from which moment we need to take the weather for 12 hours
        time = pd.Timestamp.now().round('60min').to_pydatetime().timestamp()
        # The weather update did not include Sumy and Lviv, so here is a replacement name for these two cities
        if(city == "Sumy"):
            generateRegionPredict("Sumy Oblast", region_id, time).to_csv("predictioninfo/" + city + "/" + str(time) + '.csv', index=False)
        elif(city == "Lviv"):
            generateRegionPredict("L'viv", region_id, time).to_csv("predictioninfo/" + city + "/" + str(time) + '.csv',index=False)
        else:
            #Generate a forecast for the next 12 hours for a specific city and save it to .csv
            generateRegionPredict(city, region_id, time).to_csv("predictioninfo/"+city+"/"+str(time)+'.csv', index=False)
        # Create or recreate a document in which we record the time for which the last forecast was generated
        # in the Epoch format, because we record forecasts with this name, so it will greatly simplify the opening of the document for further api
        f = open("predictioninfo/lastHour.txt", "w")
        f.write(str(time))
        f.close()
        # Create or re-create a document in which we record the time of the last forecast generation completion
        f2 = open("predictioninfo/lastUpdate.txt", "w")
        f2.write(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        f2.close()

def generateRegionPredict(city, region_id, time):
    # Generate weather for the city by calling the code with the weather
    df = gw.getWeatherForecast(city)
    # Add the region number required for the forecast to each line
    df.insert(loc=len(df.columns) - 1, column='region_id', value=region_id)
    # Видаляємо не актуальні погодні дані(якщо прогноз на 12, то нам не потрібен прогноз на 11 і тд)
    removeOld = df.loc[df['hour_datetimeEpoch'] >= time].sort_values(by=['hour_datetimeEpoch'])
    # take the next 12 hours after removing outdated ones
    hours12 = removeOld.head(12)
    # we get an array with the days to which the hours belong (23 00 belongs to one day, and 00 to another. if there is only one day, then there will be an array with
    # 1 element),
    # to know which vectors we need
    daysForVectors = hours12['day_datetime'].unique()
    # get a dataset with vectors (if only one day is needed, then a dataset with only 1 row)
    vectorDF = generateVectorDF(daysForVectors)
    # combine datasets with the weather and the resulting vectors by day
    merge = hours12.merge(vectorDF, left_on='day_datetime', right_on='date')
    # remove the fields with the day, as they are not needed for the forecast
    merge = merge.drop(['day_datetime', 'date'], axis=1)
    # replace all NaNs with 0
    merge = merge.fillna(0)
    # change the type of column headers to String, because this is what the model wants
    merge.columns = merge.columns.astype(str)
    # Create a dataset with one column with time
    Epoch = merge['hour_datetimeEpoch']
    # Our data is very different, so we used scaling to improve the prediction and upload it here
    # a model that is already trained to scale
    scaler = pickle.load(open(f"{MODEL_FOLDER}/scaler.pkl", "rb"))
    # scale results using the previous model
    merge = pd.DataFrame(scaler.transform(merge), columns=merge.columns)
    # load the model for predicting alarms
    model = pickle.load(open(MODEL_FOLDER+MODEL_FILE, "rb"))
    # make a prediction that returns 12 True or False
    res = model.predict(merge)
    # create the final dataset, what we will return over time and whether there will be an alarm
    time = pd.DataFrame({'Time': Epoch, 'alarm': res})
    # create a time column that will convert Epoch to a date, but it will be Greenwich Mean Time
    time['date'] = pd.to_datetime(time['Time'], unit='s')
    # Overwrite the Time column by taking the time from date and changing the time zone to Kyiv
    time['Time'] = time['date'].dt.tz_localize(pytz.utc).dt.tz_convert('Europe/Kyiv').apply(lambda x: x.replace(tzinfo=None))
    # Delete the temporary date column
    time = time.drop(['date'], axis=1)
    return time



def generateVectorDF(daysForVectors):
    # create an empty dataset for vectors
    vectorDF = pd.DataFrame()
    # go through the received days for which you need to get a forecast
    for i in daysForVectors:
        # we need the forecast for the previous day, so we find its date
        previousDate = datetime.datetime.strptime(i, '%Y-%m-%d') - datetime.timedelta(days=1)
        # get the required vector
        temp = gv.GetVector(previousDate.strftime('%Y-%m-%d'))
        # add to the vector the day for which it is assigned (report for 01.04.23 to predict 02.04.23)
        temp.insert(loc=0, column='date', value=[i])
        # add a vector to our dataframe
        vectorDF = pd.concat([vectorDF, temp], axis=0)
    return vectorDF

# generate forecasts for all regions
generateAllRegionPredictions()
