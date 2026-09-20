from extraction.bronze import run_bronze

from transformation.silver import run_silver

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

print("Gold is ready to dev")