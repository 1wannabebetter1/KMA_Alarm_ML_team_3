# Code done by Yefremenko Anastasiia

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../data/weather/all_weather_by_hour.csv')

# correlation between wind speed and time

x = 'day_datetimeEpoch'
y = 'day_windspeed'
plot = df.plot(kind='scatter', x=x, y=y)

plot.set_xlabel("Datetime Epoch")
plot.set_ylabel("Wind speed")
plot.set_title("Correlation between wind speed and time")

plt.show()