
import pandas as pd
import matplotlib.pyplot as plt

# Зчитуємо дані з файлу
df = pd.read_csv("data/events/alarms.csv", sep=";")

# Перетворюємо колонки "start" та "end" у формат дати та часу
df["start"] = pd.to_datetime(df["start"])
df["end"] = pd.to_datetime(df["end"])

# Розраховуємо тривалість тривоги в годинах
df["duration"] = (df["end"] - df["start"]).dt.total_seconds() / 3600

# Групуємо дані за датою та розраховуємо середнє значення тривалості тривоги
grouped_data = df.groupby(df["start"].dt.date)["duration"].mean()

# Побудова графіку
fig, ax = plt.subplots(figsize=(15, 10))
ax.plot(grouped_data.index, grouped_data.values, color="blue")
ax.set_xlabel("Дата")
ax.set_ylabel("Тривалість тривоги (години)")
ax.set_title("Середня тривалість тривоги")
plt.show()