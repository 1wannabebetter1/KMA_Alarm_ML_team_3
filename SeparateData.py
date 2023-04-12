# Developed by Maksym Polishchuk
import pandas as pd


def separate():

    # df = pd.read_csv('data/merged_dataset/all_info_with_tfidf.csv', sep=';')
    df = pd.read_csv('data/merged_dataset/all_info_with_tfidf.csv', sep=';', nrows=20000)

    dates = pd.to_datetime(df['hour_datetimeEpoch'], unit='s')

    min_date = dates.min()
    max_date = dates.max()

    train_time_percent = .75
    between_min_max = max_date - min_date
    end_date_train = min_date + train_time_percent * between_min_max

    x_train_df = df[pd.to_datetime(df.hour_datetimeEpoch, unit='s') <= end_date_train]
    x_test_df = df[pd.to_datetime(df.hour_datetimeEpoch, unit='s') > end_date_train]

    y_train_df = x_train_df['isAlarm']
    y_test_df = x_test_df['isAlarm']

    # x_train_df.drop(['isAlarm'], axis=1, inplace=True)
    # x_test_df.drop(['isAlarm'], axis=1, inplace=True)

    x_train_df = x_train_df.drop(['isAlarm'], axis=1)
    x_test_df = x_test_df.drop(['isAlarm'], axis=1)

    # x_train_df.to_csv('x_train.csv', index=False)
    # y_train_df.to_csv('y_train.csv', index=False)
    # x_test_df.to_csv('x_test.csv', index=False)
    # y_test_df.to_csv('y_test.csv', index=False)

    return x_train_df, y_train_df, x_test_df, y_test_df


# x_train, y_train, x_test, y_test = separate()
# print(x_train)
# print(y_train)
# print(x_test)
# print(y_test)
