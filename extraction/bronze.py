import json
import requests
import pandas as pd


def get_data(path):
    return pd.read_csv(path)


def store_cities(cities, path):
    cities.to_csv(f"{path}/cities/cities.csv", index=False)


def prepare_url(lat, lng):
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
        "timezone": "auto",
    }

    response = requests.get("https://api.open-meteo.com/v1/forecast", params=params)

    response.raise_for_status()

    return response


def extract_weather(cities):
    weather_data = []

    for _, city in cities.iterrows():
        print(f"Get {city["city"]}...")

        response = prepare_url(city["lat"], city["lng"])

        weather_data.append({"city": city["city"], "data": response.json()})

        print(f"Success {city["city"]}")

    return weather_data


def store_weather(weather_data, path):
    with open(f"{path}/weather/weather.json", "w", encoding="utf-8") as file:
        json.dump(weather_data, file, indent=2)


def run_bronze(origine, bronze):
    print("Start Bronze part...")

    cities = get_data(origine)

    store_cities(cities, bronze)

    weather_data = extract_weather(cities)

    store_weather(weather_data, bronze)

    print("Finish Bronze part")
