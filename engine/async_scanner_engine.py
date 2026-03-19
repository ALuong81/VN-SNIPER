import asyncio
from data.symbol_loader import load_symbols
import pandas as pd

async def fetch_stock_data(symbol: str) -> dict:
    """
    Async fetch dữ liệu stock từ API.
    """
    # TODO: thay endpoint bằng API thật
    await asyncio.sleep(0.05)  # mô phỏng network latency
    return {"symbol": symbol, "price": 100.0}

async def scan_market_async(limit: int = 120):
    """
    Quét thị trường, lọc symbol valid, fallback sector.
    Trả về stocks và sector_map
    """
    df = load_symbols(limit=limit)
    
    # Tạo map sector
    sector_map = dict(zip(df['symbol'], df['sector']))

    stocks = []

    # Async fetch tất cả symbol
    tasks = [fetch_stock_data(sym) for sym in df['symbol']]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for res, sym in zip(results, df['symbol']):
        if isinstance(res, Exception):
            print(f"⚠ ERROR: symbol {sym} fetch failed: {res}")
        else:
            stocks.append(res)

    return stocks, sector_map

# Test chạy trực tiếp
if __name__ == "__main__":
    import asyncio
    stocks, sector_map = asyncio.run(scan_market_async(limit=10))
    print(stocks)
    print(sector_map)