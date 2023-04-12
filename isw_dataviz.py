import pandas as pd
import re
import matplotlib.pyplot as plt

# читаємо таблицю alarms з файлу
alarms_df = pd.read_csv("data/events/alarms.csv", delimiter=";")

# визначаємо місяці для кожного запису в таблиці alarms
alarms_df["month"] = pd.to_datetime(alarms_df["start"]).dt.month

# знаходимо місяць з найбільшою кількістю тривог
most_alarms_month = alarms_df["month"].value_counts().idxmax()

# виводимо місяць з найбільшою кількістю тривог
print(f"Місяць з найбільшою кількістю тривог: {most_alarms_month}")

# читаємо таблицю lemm_and_stemm з файлу та видаляємо слова зі стовпчика lemm
lemm_and_stemm_df = pd.read_csv("data/lemm_stemm_vect/lemm_and_stemm.csv", delimiter=";")
lemm_and_stemm_df["lemm"] = lemm_and_stemm_df["lemm"].apply(lambda x: re.sub(r'\b(are|the|she|they|has|had|been|for|The|and|from|that)\b', '', str(x)))

# створюємо маску для вибору записів з найбільшою кількістю тривог
mask = alarms_df["month"] == most_alarms_month


# вибираємо записи з маскою та робимо об'єднання стовпців зі стовпцем lemm з таблиці lemm_and_stemm
words = ' '.join(lemm_and_stemm_df[mask]["lemm"].str.cat(sep=' ').split())

# створюємо список слів, що складаються з більше 2 літер
words_list = re.findall(r'\b\w{3,}\b', words)

# знаходимо найчастіше вживане слово
most_common_word = max(set(words_list), key = words_list.count)

# виводимо найчастіше вживане слово
print(f"Найчастіше вживане слово: {most_common_word}")

# рахуємо кількість кожного слова
word_counts = pd.Series(words_list).value_counts()

# створюємо кругову діаграму найчастіше вживаного слова
plt.figure(figsize=(15,10))
plt.pie(word_counts[:10], labels=word_counts[:10].index, autopct='%1.1f%%')
plt.title(f"Найчастіше вживані слова у місяці {most_alarms_month}")
plt.show()
