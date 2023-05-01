# Code done by Yefremenko Anastasiia

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../data/weather/all_weather_by_hour.csv')

# correlation with datetime and pressure
x = 'day_datetimeEpoch'
y = 'day_pressure'
plot = df.plot(kind='scatter', x=x, y=y)

plot.set_xlabel("Datetime Epoch")
plot.set_ylabel("Pressure")
plot.set_title("Correlation between pressure and time")

plt.show()