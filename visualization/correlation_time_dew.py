# Code done by Yefremenko Anastasiia

import pandas as pd
import matplotlib.pyplot as plt

#reads csv
df = pd.read_csv('../data/weather/all_weather_by_hour.csv')

# correlation with datetime Epoch and dew in a day
x = 'day_datetimeEpoch'
y = 'day_dew'
plot = df.plot(kind='scatter', x=x, y=y)

# names
plot.set_xlabel("Datetime Epoch")
plot.set_ylabel("Dew")
plot.set_title("Correlation between dew in a day and date")

plt.show()
