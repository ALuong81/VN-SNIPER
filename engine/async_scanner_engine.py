import asyncio
from data.market_data import load_stock
from data.symbol_loader import load_symbols
from utils.sector_utils import fetch_sector_map


async def fetch(symbol):
    try:
        return await asyncio.to_thread(load_stock, symbol)
    except Exception as e:
        return None


async def scan_market_async():

    print("STEP 1: SCAN MARKET")

    # 🔹 Load danh sách symbol
    symbols = load_symbols(limit=120)

    if not symbols:
        print("❌ No symbols")
        return [], {}   # luôn return 2 giá trị

    print(f"Universe loaded: {len(symbols)}")

    # 🔹 Giới hạn concurrent
    semaphore = asyncio.Semaphore(10)

    async def sem_fetch(s):
        async with semaphore:
            return await fetch(s)

    # 🔹 Fetch dữ liệu async
    tasks = [sem_fetch(s) for s in symbols]
    results = await asyncio.gather(*tasks)

    # 🔹 Lọc dữ liệu hợp lệ
    stocks = [r for r in results if r]

    print(f"Loaded OK: {len(stocks)} | Failed: {len(symbols) - len(stocks)}")

    if not stocks:
        print("❌ No stock data")
        return [], {}

    # 🔥 ===== SECTOR INTELLIGENCE =====

    symbol_list = [s["symbol"] for s in stocks]

    print("Fetching sector data...")

    sector_map = fetch_sector_map(symbol_list)

    # 🔹 Gán sector vào từng stock
    for s in stocks:
        symbol = s["symbol"]
        s["sector"] = sector_map.get(symbol, "KHÁC")

    # 🔹 Debug nhanh (rất nên giữ)
    sample = list(sector_map.items())[:5]
    print(f"Sample sector: {sample}")

    # 🔹 Thống kê nhanh
    sector_count = {}
    for s in stocks:
        sector = s["sector"]
        sector_count[sector] = sector_count.get(sector, 0) + 1

    top_sector = sorted(sector_count.items(), key=lambda x: x[1], reverse=True)[:3]
    print(f"Top sectors (raw): {top_sector}")

    # 🔥 RETURN CHUẨN (QUAN TRỌNG)
    return stocks, sector_map
