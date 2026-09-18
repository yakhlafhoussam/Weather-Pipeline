import pandas as pd


def get_data(path):
    return pd.read_csv(path)


def store_cities(cities, path):
    cities.to_csv(
        f"{path}/cities/cities.csv",
        index=False
    )