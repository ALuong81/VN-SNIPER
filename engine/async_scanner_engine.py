import asyncio
from data.market_data import load_stock

SYMBOLS = []  # load từ listing

async def fetch(symbol):
    return load_stock(symbol)

async def scan_market_async():

    tasks = [fetch(s) for s in SYMBOLS[:150]]

    results = await asyncio.gather(*tasks)

    stocks = [r for r in results if r]

    print(f"Loaded OK: {len(stocks)}")

    return stocks
