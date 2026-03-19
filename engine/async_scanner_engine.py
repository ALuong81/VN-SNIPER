import asyncio
import random

from data.market_data import load_stock
from data.symbol_loader import load_symbols


async def fetch(symbol):

    for attempt in range(3):
        try:
            data = await asyncio.to_thread(load_stock, symbol)

            if not data or "close" not in data:
                raise ValueError("Invalid data")

            return data

        except Exception as e:
            print(f"[RETRY {attempt+1}] {symbol}")
            await asyncio.sleep(0.3)

    return None


async def scan_market_async(limit=120):

    print("STEP 1: SCAN MARKET")

    symbols, sector_map = load_symbols()

    print(f"Universe loaded: {len(symbols)}")

    # 🔥 FIX BIAS
    random.shuffle(symbols)

    symbols = symbols[:limit]

    print(f"Symbols to load: {len(symbols)}")

    tasks = [fetch(s) for s in symbols]

    results = await asyncio.gather(*tasks)

    stocks = []

    for r in results:
        if isinstance(r, dict):
            stocks.append(r)

    print(f"Loaded OK: {len(stocks)} | Failed: {len(symbols) - len(stocks)}")

    return stocks, sector_map
