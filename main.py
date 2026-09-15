import pandas as pd

df = pd.read_csv("sources/worldcities.csv")
morocco = df[df["country"] == "Morocco"]

morocco.to_csv("morocco_cities.csv", index=False)