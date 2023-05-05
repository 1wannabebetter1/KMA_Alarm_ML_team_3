# Code done by Yefremenko Anastasiia

import pandas as pd
import matplotlib.pyplot as plt

# reads csv
df = pd.read_csv('../data/weather/all_weather_by_hour.csv')

# plot correlation between datetime Epoch and humidity
x = 'day_datetimeEpoch'
y = 'day_humidity'
plot = df.plot(kind='scatter', x=x, y=y)

# names
plot.set_xlabel("Datetime Epoch")
plot.set_ylabel("Humidity")
plot.set_title("Correlation between humidity and time")

plt.show()
