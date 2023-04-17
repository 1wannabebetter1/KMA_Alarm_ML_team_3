# Code done by Yefremenko Anastasiia

import pandas as pd
import matplotlib.pyplot as plt

#read csv
df = pd.read_csv('/Users/anastasia/Desktop/programming python/data/merged_dataset/new_features_copy.csv', sep=';')

# correlation with datetime and alerts_last_24h
x = 'day_datetime'
y = 'alerts_last_24h_all_reg'

plot = df.plot(kind='scatter', x=x, y=y)

plot.set_xlabel("Datetime")
plot.set_ylabel("Frequency of alerts")
plot.set_title("Distribution of alerts in a last 24 hours in all regions")

plt.show()