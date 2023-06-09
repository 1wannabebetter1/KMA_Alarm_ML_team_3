# Code done by Yefremenko Anastasiia

import pandas as pd
import matplotlib.pyplot as plt

# reads csv
df = pd.read_csv('../data/weather/all_weather_by_hour.csv')

x = 'day_datetimeEpoch'
y = 'day_solarradiation'

# draws plot
plot = df.plot(kind='scatter', x=x, y=y)

# names
plot.set_xlabel("Datetime Epoch")
plot.set_ylabel("Solar radiation")
plot.set_title("Correlation between solar radiation in a day and time")

plt.show()

