import asyncio
from data.market_data import load_stock

SYMBOLS = ["VCG", "HBC", "VND", "SSI", "VIC"]


# ===== WRAP SYNC → ASYNC =====
async def fetch(symbol):

    for attempt in range(3):
        try:
            data = await asyncio.to_thread(load_stock, symbol)

            if not data or "close" not in data:
                raise ValueError("Invalid data")

            return data

        except Exception as e:
            print(f"[RETRY {attempt+1}] {symbol} - {str(e)}")
            await asyncio.sleep(0.5)

    return None


# ===== MAIN SCAN =====
async def scan_market_async():

    print("Start loading...")

    semaphore = asyncio.Semaphore(10)  # limit concurrent

    async def sem_fetch(s):
        async with semaphore:
            return await fetch(s)

    tasks = [sem_fetch(s) for s in SYMBOLS]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    stocks = []

    for r in results:
        if isinstance(r, dict):
            stocks.append(r)

    print(f"Loaded OK: {len(stocks)}")

    return stocks
