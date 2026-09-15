import pandas as pd

def getData(path):
    df = pd.read_csv(path)
    return df

def storeCities(cities, path):
    cities.to_csv(f"{path}cities/cities.csv", index=False)

def prepareUrl(lat, lng):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&hourly=temperature_2m"
    return url

origine = "sources/ma.csv"
bronze = "data/bronze/"
silver = "data/silver/"
gold = "data/gold/"

cities = getData(origine)
storeCities(cities, bronze)