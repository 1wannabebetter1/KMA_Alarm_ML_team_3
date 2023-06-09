# Code done by Yefremenko Anastasiia

import pandas as pd
import matplotlib.pyplot as plt

#read csv
df = pd.read_csv('../data/merged_dataset/new_features.csv', sep=';')

# correlation with datetime and alerts_last_24h
x = 'day_datetime'
y = 'alerts_last_24h_all_reg'

# draws plot
plot = df.plot(kind='scatter', x=x, y=y)

# names
plot.set_xlabel("Datetime")
plot.set_ylabel("Frequency of alerts")
plot.set_title("Distribution of alerts in a last 24 hours in all regions")

plt.show()
