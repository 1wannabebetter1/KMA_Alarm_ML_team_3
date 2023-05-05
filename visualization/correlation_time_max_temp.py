# Code done by Yefremenko Anastasiia

import pandas as pd
import matplotlib.pyplot as plt

# reads csv
df = pd.read_csv('../data/weather/all_weather_by_hour.csv')

# draws plot correlation with datetime Epoch and temperature
x = 'day_datetimeEpoch'
y = 'day_tempmax'
plot = df.plot(kind='scatter', x=x, y=y)

# names
plot.set_xlabel("Datetime Epoch")
plot.set_ylabel("Maximum temperature")
plot.set_title("Correlation between maximum temperature and time")

plt.show()
