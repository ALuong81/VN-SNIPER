import pandas as pd
import aiohttp
import asyncio

VNSTOCK_API = "https://finfo-api.vndirect.com.vn/v4/quotes"
BATCH_SIZE = 50
MAX_RETRY = 3
RETRY_DELAY = 2  # giây

async def fetch_batch(session, symbols_batch):
    """
    Lấy giá close cho 1 batch với retry và log chi tiết
    """
    for attempt in range(1, MAX_RETRY + 1):
        try:
            params = {"symbols": ",".join(symbols_batch)}
            async with session.get(VNSTOCK_API, params=params) as resp:
                data = await resp.json()
                closes = {}
                for item in data.get("data", []):
                    sym = item.get("symbol")
                    closes[sym] = item.get("close", 0.0)
                # đảm bảo tất cả symbol đều có giá
                for s in symbols_batch:
                    if s not in closes:
                        closes[s] = 0.0
                print(f"✅ Batch success (attempt {attempt}): {len(symbols_batch)} symbols")
                return closes
        except Exception as e:
            print(f"⚠ Batch attempt {attempt} failed: {str(e)}")
            if attempt < MAX_RETRY:
                await asyncio.sleep(RETRY_DELAY)
            else:
                print(f"❌ Batch failed after {MAX_RETRY} attempts, assigning 0 for all")
                return {s: 0.0 for s in symbols_batch}

async def load_symbols_retry_log(limit=None):
    """
    Load danh sách symbol + giá close batch async với retry và log chi tiết
    """
    df = pd.read_csv("data/full_symbols.csv")

    if 'sector' not in df.columns:
        df['sector'] = 'KHÁC'
    if 'exchange' not in df.columns:
        df['exchange'] = 'VN'

    if limit is not None:
        df = df.head(limit)

    symbols = df['symbol'].tolist()
    closes = {}

    async with aiohttp.ClientSession() as session:
        for i in range(0, len(symbols), BATCH_SIZE):
            batch = symbols[i:i+BATCH_SIZE]
            print(f"🔹 Fetching batch {i//BATCH_SIZE + 1}: {batch}")
            batch_closes = await fetch_batch(session, batch)
            closes.update(batch_closes)

    df['close'] = df['symbol'].map(closes)
    stocks = df.to_dict('records')
    sector_map = dict(zip(df['symbol'], df['sector']))
    return stocks, sector_map
