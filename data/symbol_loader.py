# data/symbol_loader.py
import pandas as pd

df = pd.read_csv("data/full_symbols.csv")

symbols = df["symbol"].tolist()
sector_map = dict(zip(df["symbol"], df["sector"]))

def load_symbols(limit=None):
    """
    Trả về danh sách symbol, có thể giới hạn số lượng bằng limit
    """
    if limit is None:
        return symbols
    return symbols[:limit]

def get_sector_map():
    return sector_map
