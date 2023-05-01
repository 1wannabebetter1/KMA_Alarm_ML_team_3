# Code done by Yefremenko Anastasiia

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm

# read csv 
df = pd.read_csv('../data/merged_dataset/new_features.csv', sep=';')

# remove duplicate rows
df = df.drop_duplicates(subset=['region_id', 'isAlarm', 'day_datetime'])

# group by region_id and sum regions_with_alert
df_sum = df.query('isAlarm == True').groupby('region_id', as_index=False)['regions_with_alert'].sum()

x = 'region_id'
y = 'regions_with_alert'

# create histogram
plot = df_sum.plot(kind="bar", x=x, y=y,
                   color=cm.YlOrRd(df_sum['regions_with_alert'] / max(df_sum['regions_with_alert'])))

# names
plot.set_xlabel("Region")
plot.set_ylabel("Frequency of alerts")
plot.set_title("Hours with alerts")

plt.show()
