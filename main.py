import pandas as pd
import requests
import json
from pathlib import Path

#=================================Bronze=======================================

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
        "forecast_days": 3,
        "timezone": "auto"
    }
    
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params=params
    )
    response.raise_for_status()
    
    return response

origine = "sources/ma.csv"
bronze = "data/bronze"
silver = "data/silver"
gold = "data/gold"

#=================================Bronze=======================================

# cities = getData(origine)
# storeCities(cities, bronze)

weather_data = []

# for _, col in cities.iterrows():
#     response = prepareUrl(col["lat"], col["lng"])
#     data = response.json()

#     weather_data.append({
#         "city": col["city"],
#         "data": data
#     })

# with open(f"{bronze}/weather/weather.json", "w") as f:
#     json.dump(weather_data, f, indent=2)

with open(f"{bronze}/weather/weather.json", "r") as f:
    weather_data = json.loads(f.read())

#=================================Silver=======================================

rows = []

for city_data in weather_data:
    city = city_data["city"]
    daily = city_data["data"]["daily"]
    for i in range(len(daily["time"])):
        rows.append({
            "city": city,
            "date": daily["time"][i],
            "temperature_max": daily["temperature_2m_max"][i],
            "temperature_min": daily["temperature_2m_min"][i],
            "precipitation_sum": daily["precipitation_sum"][i],
            "precipitation_probability_max": daily["precipitation_probability_max"][i],
            "wind_speed_max": daily["wind_speed_10m_max"][i],
            "wind_gusts_max": daily["wind_gusts_10m_max"][i],
            "weather_code": daily["weather_code"][i]
        })

df = pd.DataFrame(rows)

df["date"] = pd.to_datetime(df["date"])

df = df.drop_duplicates()

df = df[df["temperature_2m_min"] <= df["temperature_2m_max"]]

df = df.dropna()

df = df[
    (df["precipitation_sum"] >= 0)
    & (df["wind_speed_10m_max"] >= 0)
]

df.to_csv(f"{silver}/weather_clean.csv", index=False)