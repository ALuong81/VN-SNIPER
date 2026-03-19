import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor


CACHE_PATH = "sector_cache.json"


def load_sector_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    return {}


def save_sector_cache(sector_map):
    with open(CACHE_PATH, "w") as f:
        json.dump(sector_map, f)


def fetch_sector(symbol):
    try:
        url = f"https://restv2.fireant.vn/symbols/{symbol}"
        res = requests.get(url, timeout=5)
        if res.status_code != 200:
            return symbol, "KHÁC"

        data = res.json()
        return symbol, data.get("sectorName", "KHÁC")

    except:
        return symbol, "KHÁC"


def fetch_sector_map(symbols):
    cache = load_sector_cache()

    # chỉ fetch những mã chưa có
    missing = [s for s in symbols if s not in cache]

    if missing:
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(fetch_sector, missing)

        for symbol, sector in results:
            cache[symbol] = sector

        save_sector_cache(cache)

    return cache
