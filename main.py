from extraction.bronze import run_bronze

from transformation.silver import run_silver

from transformation.gold import run_gold

origine = "sources/ma.csv"

bronze = "data/bronze"
silver = "data/silver"
gold = "data/gold"

# =========================
# Bronze
# =========================

run_bronze(origine, bronze)

# =========================
# Silver
# =========================

run_silver(f"{bronze}/weather/weather.json", f"{silver}/weather_clean.csv")

# =========================
# Gold
# =========================

run_gold(f"{silver}/weather_clean.csv", f"{gold}/weather_gold.csv")