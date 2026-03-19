import asyncio
from data.market_data import load_stock
from data.symbol_loader import load_symbols


INVALID_CACHE = set()


async def fetch(item):

    symbol = item["symbol"]

    if symbol in INVALID_CACHE:
        return None

    for attempt in range(2):
        try:
            data = await asyncio.to_thread(load_stock, symbol)

            if not data or "close" not in data:
                raise ValueError("Invalid data")

            # gắn metadata từ CSV
            data["sector"] = item["sector"]
            data["exchange"] = item["exchange"]

            return data

        except Exception as e:
            print(f"[FAIL] {symbol}")
            INVALID_CACHE.add(symbol)
            return None

    return None


async def scan_market_async(limit=120):

    print("STEP 1: SCAN MARKET")

    universe = load_symbols()

    if not universe:
        print("❌ No symbols")
        return []

    # 👉 ưu tiên HOSE trước
    universe = sorted(universe, key=lambda x: x["exchange"])

    symbols_to_load = universe[:limit]

    print(f"Symbols to load: {len(symbols_to_load)}")

    semaphore = asyncio.Semaphore(10)

    async def sem_fetch(s):
        async with semaphore:
            return await fetch(s)

    tasks = [sem_fetch(s) for s in symbols_to_load]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    stocks = []

    for r in results:
        if isinstance(r, dict):
            stocks.append(r)

    print(f"Loaded OK: {len(stocks)} | Failed: {len(symbols_to_load) - len(stocks)}")

    return stocks
