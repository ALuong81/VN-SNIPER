from data.async_symbol_loader_retry_log import load_symbols_retry_log

async def scan_market_async():
    # lấy tối đa 120 symbol
    stocks, sector_map = await load_symbols_retry_log(limit=120)
    return stocks, sector_map
