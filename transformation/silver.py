import json
import pandas as pd


def load_weather(path):
    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def flatten_weather(weather_data):
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
                "precipitation_probability_max":
                    daily["precipitation_probability_max"][i],
                "wind_speed_max":
                    daily["wind_speed_10m_max"][i],
                "wind_gusts_max":
                    daily["wind_gusts_10m_max"][i],
                "weather_code":
                    daily["weather_code"][i]
            })

    return pd.DataFrame(rows)


def clean_weather(df):

    df["date"] = pd.to_datetime(
        df["date"]
    )

    df = df.drop_duplicates()

    df = df[
        df["temperature_min"]
        <= df["temperature_max"]
    ]

    df = df.dropna()
    
    df = df[
        (df["precipitation_sum"] >= 0)
        & (df["wind_speed_max"] >= 0)
    ]

    return df


def save_silver(df, path):

    df.to_csv(
        path,
        index=False
    )


def run_silver(
    weather_path,
    output_path
):

    weather_data = load_weather(
        weather_path
    )

    df = flatten_weather(
        weather_data
    )

    df = clean_weather(
        df
    )

    save_silver(
        df,
        output_path
    )