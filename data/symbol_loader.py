import pandas as pd

df = pd.read_csv("data/full_symbols.csv")

symbols = df["symbol"].tolist()
sector_map = dict(zip(df["symbol"], df["sector"]))

def load_symbols():
    return symbols

def detect_sector(symbol):
    return sector_map.get(symbol, "KHÁC")
