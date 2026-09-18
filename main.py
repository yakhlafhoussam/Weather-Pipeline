from extraction.cities import (
    get_data,
    store_cities
)

from extraction.weather import (
    extract_weather,
    store_weather
)

from transformation.silver import (
    run_silver
)

from transformation.gold import (
    run_gold
)


origine = "sources/ma.csv"

bronze = "data/bronze"
silver = "data/silver"
gold = "data/gold"


# =========================
# Bronze
# =========================

cities = get_data(
    origine
)

store_cities(
    cities,
    bronze
)

weather_data = extract_weather(
    cities
)

store_weather(
    weather_data,
    bronze
)


# =========================
# Silver
# =========================

run_silver(
    f"{bronze}/weather/weather.json",
    f"{silver}/weather_clean.csv"
)


# =========================
# Gold
# =========================

run_gold(
    f"{silver}/weather_clean.csv",
    f"{gold}/weather_features.csv"
)