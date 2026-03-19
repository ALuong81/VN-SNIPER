import pandas as pd

df = pd.read_csv("data/full_symbols.csv")

sector_map = dict(zip(df["symbol"], df["sector"]))


def detect_sector(symbol):
    return sector_map.get(symbol, "KHÁC")


def sector_top(stocks):

    score_map = {}

    for s in stocks:
        sec = s.get("sector", "KHÁC")
        score_map[sec] = score_map.get(sec, 0) + s.get("meta_score", 0)

    return sorted(score_map.items(), key=lambda x: x[1], reverse=True)[:3]
