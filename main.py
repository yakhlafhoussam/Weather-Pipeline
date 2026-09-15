import pandas as pd

def getData():
    df = pd.read_csv("sources/ma.csv")
    return df

def storeCities(cities, path):
    cities.to_csv(f"{path}cities.csv", index=False)

bronze = "data/bronze/"
silver = "data/silver/"
gold = "data/gold/"

cities = getData()
storeCities(cities, bronze)