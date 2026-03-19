import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor
from data.sector_map_full import SECTOR_DATA

CACHE_PATH = "sector_cache.json"

def resolve_sector(symbol, cache):

    # cache
    if symbol in cache:
        return cache[symbol]

    # dataset local (ưu tiên cao)
    if symbol in SECTOR_DATA:
        return SECTOR_DATA[symbol]

    # API (optional)
    sector = fetch_sector_api(symbol)
    if sector:
        cache[symbol] = sector
        return sector

    return "KHÁC"
    
def load_sector_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    return {}


def save_sector_cache(cache):
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f)


def fetch_sector_api(symbol):
    try:
        url = f"https://restv2.fireant.vn/symbols/{symbol}"
        res = requests.get(url, timeout=5)

        if res.status_code != 200:
            return None

        data = res.json()

        return data.get("industryName") or data.get("sectorName")

    except:
        return None


def resolve_sector(symbol, cache):
    # Priority 1: Cache
    if symbol in cache:
        return cache[symbol]

    # Priority 2: API
    sector = fetch_sector_api(symbol)
    if sector:
        cache[symbol] = sector
        return sector

    # Priority 3: Local dataset
    if symbol in SECTOR_DATA:
        return SECTOR_DATA[symbol]

    # Final fallback
    return "KHÁC"


def fetch_sector_map(symbols):
    cache = load_sector_cache()

    def process(symbol):
        sector = resolve_sector(symbol, cache)
        return symbol, sector

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(process, symbols)

    sector_map = dict(results)

    save_sector_cache(cache)

    return sector_map
