import os
import pandas as pd
import psycopg

def save_data():

    # Connect to PostgreSQL
    connection = psycopg.connect(
        host="postgres",
        port=5432,
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    cursor = connection.cursor()


    # =========================
    # Load cities
    # =========================

    cities = pd.read_csv("../data/bronze/cities/cities.csv")

    for row in cities.itertuples(index=False):

        cursor.execute(
            """
            INSERT INTO city (
                id, city, city_ascii, lat, lng,
                country, iso2, admin_name,
                capital, population
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """,
            (
                row.id,
                row.city,
                row.city_ascii,
                row.lat,
                row.lng,
                row.country,
                row.iso2,
                row.admin_name,
                row.capital,
                row.population,
            ),
        )


    # =========================
    # Load weather
    # =========================

    weather = pd.read_csv("../data/gold/weather_gold.csv")

    for row in weather.itertuples(index=False):

        cursor.execute("SELECT id FROM city WHERE city = %s", (row.city,))

        city_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO weather (
                city_id,
                date,
                temperature_max,
                temperature_min,
                precipitation_sum,
                precipitation_probability_max,
                wind_speed_max,
                wind_gusts_max,
                weather_code,
                temperature_category,
                precipitation_category,
                wind_category,
                precipitation_risk,
                wind_risk,
                temperature_risk,
                risk_score,
                risk_category
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (city_id, date) DO NOTHING
        """,
            (
                city_id,
                row.date,
                row.temperature_max,
                row.temperature_min,
                row.precipitation_sum,
                row.precipitation_probability_max,
                row.wind_speed_max,
                row.wind_gusts_max,
                row.weather_code,
                row.temperature_category,
                row.precipitation_category,
                row.wind_category,
                row.precipitation_risk,
                row.wind_risk,
                row.temperature_risk,
                row.risk_score,
                row.risk_category,
            ),
        )


    connection.commit()

    cursor.close()
    connection.close()

    print("Data loaded successfully!")
