import pandas as pd

df = pd.read_csv("sources/ma.csv")

df.to_csv("data/bronze/cities", index=False)