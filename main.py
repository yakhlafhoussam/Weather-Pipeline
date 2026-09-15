import pandas as pd
import requests

def getData(path):
    df = pd.read_csv(path)
    return df

def storeCities(cities, path):
    cities.to_csv(f"{path}/cities/cities.csv", index=False)

def prepareUrl(lat, lng):
    params = {
        "latitude": lat,
        "longitude": lng,
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_sum,"
            "precipitation_probability_max,"
            "wind_speed_10m_max,"
            "wind_gusts_10m_max,"
            "weather_code"
        ),
        "forecast_days": 7,
        "timezone": "auto"
    }

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params=params
    )

    return response

origine = "sources/ma.csv"
bronze = "data/bronze"
silver = "data/silver"
gold = "data/gold"

cities = getData(origine)
storeCities(cities, bronze)

for _, col in cities.iterrows():
    response = prepareUrl(col["lat"], col["lng"])
    with open(f"{bronze}/weather/{col["city"]}.json", "w") as f:
        f.write(response.text)