# Code done by Yefremenko Anastasiia

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/anastasia/Desktop/programming python/data/weather/all_weather_by_hour.csv')

# correlation between datetime and humidity
x = 'day_datetimeEpoch'
y = 'day_humidity'
plot = df.plot(kind='scatter', x=x, y=y)

plot.set_xlabel("Datetime Epoch")
plot.set_ylabel("Humidity")
plot.set_title("Correlation between humidity and time")

plt.show()