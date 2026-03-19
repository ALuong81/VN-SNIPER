import asyncio
from data.market_data import load_stock
from data.symbol_loader import load_symbols


async def fetch(symbol):
    try:
        return await asyncio.to_thread(load_stock, symbol)
    except:
        return None


async def scan_market_async():

    print("STEP 1: SCAN MARKET")

    symbols = load_symbols(limit=120)

    if not symbols:
        print("❌ No symbols")
        return []

    semaphore = asyncio.Semaphore(10)

    async def sem_fetch(s):
        async with semaphore:
            return await fetch(s)

    tasks = [sem_fetch(s) for s in symbols]

    results = await asyncio.gather(*tasks)

    stocks = [r for r in results if r]

    print(f"Loaded OK: {len(stocks)} | Failed: {len(symbols)-len(stocks)}")

    return stocks
