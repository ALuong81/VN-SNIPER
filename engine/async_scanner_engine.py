import asyncio
from data.market_data import load_stock
from data.symbol_loader import load_symbols
from utils.sector_utils import fetch_sector_map


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
        return [], {}   # 🔥 FIX: luôn return 2 giá trị

    semaphore = asyncio.Semaphore(10)

    async def sem_fetch(s):
        async with semaphore:
            return await fetch(s)

    tasks = [sem_fetch(s) for s in symbols]

    results = await asyncio.gather(*tasks)

    stocks = [r for r in results if r]

    print(f"Loaded OK: {len(stocks)} | Failed: {len(symbols)-len(stocks)}")

    # 🔥 FETCH SECTOR (THÊM MỚI)
    symbol_list = [s["symbol"] for s in stocks]

    sector_map = fetch_sector_map(symbol_list)

    # 🔥 GÁN SECTOR VÀO STOCK
    for s in stocks:
        symbol = s["symbol"]
        s["sector"] = sector_map.get(symbol, "KHÁC")

    # 🔥 RETURN CHUẨN
    return stocks, sector_map
