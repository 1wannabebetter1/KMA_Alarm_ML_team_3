# Code done by Yefremenko Anastasiia

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/anastasia/Desktop/programming python/data/weather/all_weather_by_hour.csv')

# correlation with datetime and temperature
x = 'day_datetimeEpoch'
y = 'day_tempmax'
plot = df.plot(kind='scatter', x=x, y=y)

plot.set_xlabel("Datetime Epoch")
plot.set_ylabel("Maximum temperature")
plot.set_title("Correlation between maximum temperature and time")

plt.show()