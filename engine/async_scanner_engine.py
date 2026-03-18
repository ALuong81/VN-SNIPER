import asyncio
from data.market_data import load_stock

# ===== LOAD TOÀN BỘ SYMBOL =====
def load_all_symbols():
    try:
        from vnstock import listing
        df = listing.symbols_by_exchange()

        symbols = df["symbol"].tolist()

        # lọc symbol rác
        symbols = [s for s in symbols if isinstance(s, str) and len(s) <= 3]

        print(f"Universe loaded: {len(symbols)}")

        return symbols

    except Exception as e:
        print("Load symbols error:", e)
        return []


# ===== FETCH 1 STOCK =====
async def fetch(symbol):

    for attempt in range(3):
        try:
            data = await asyncio.wait_for(
                asyncio.to_thread(load_stock, symbol),
                timeout=5
            )

            if not data or "close" not in data:
                raise ValueError("Invalid data")

            return data

        except Exception as e:
            print(f"[RETRY {attempt+1}] {symbol}")
            await asyncio.sleep(0.5)

    return None


# ===== MAIN SCAN =====
async def scan_market_async():

    print("STEP 1: SCAN MARKET")

    SYMBOLS = load_all_symbols()

    if not SYMBOLS:
        print("❌ No symbols")
        return []

    # giới hạn test nếu cần
    SYMBOLS = SYMBOLS[:500]

    print(f"Symbols to load: {len(SYMBOLS)}")

    semaphore = asyncio.Semaphore(20)

    async def sem_fetch(s):
        async with semaphore:
            return await fetch(s)

    tasks = [sem_fetch(s) for s in SYMBOLS]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    stocks = []

    for r in results:
        if isinstance(r, dict):
            stocks.append(r)

    print(f"Loaded OK: {len(stocks)} | Failed: {len(SYMBOLS) - len(stocks)}")

    return stocks
