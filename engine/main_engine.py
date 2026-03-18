import asyncio

from engine.async_scanner_engine import scan_market_async

from analysis.meta_score import score_stock
from analysis.relative_strength import calc_rs
from analysis.sector_full import detect_sector, sector_top
from analysis.sector_leader import find_sector_leaders
from analysis.market_full import market_full
from analysis.enrich_engine import enrich_stock

from signals.sniper_selector import select_sniper
from analysis.position_manager import manage_position

from report.telegram_report import send_report


# ===== MARKET RETURN =====
def calc_market_return(stocks):
    returns = []

    for s in stocks:
        try:
            c = s["close"]
            r = (c.iloc[-1] - c.iloc[-20]) / c.iloc[-20]
            returns.append(r)
        except:
            continue

    return sum(returns) / len(returns) if returns else 0


# ===== MAIN =====
def run():

    print("STEP 1: SCAN")

    stocks = asyncio.run(scan_market_async())

    if not stocks:
        print("❌ No data")
        return

    print(f"Loaded: {len(stocks)}")

    # ===== SCORE =====
    for s in stocks:
        s["meta_score"] = score_stock(s)

    # ===== FILTER SỚM =====
    stocks = [s for s in stocks if s.get("meta_score", 0) >= 50]

    if not stocks:
        print("❌ No stocks after score filter")
        return

    # ===== MARKET RETURN =====
    market_ret = calc_market_return(stocks)

    # ===== RS =====
    for s in stocks:
        s["rs"] = calc_rs(s, market_ret)

    # ===== SECTOR =====
    for s in stocks:
        s["sector"] = detect_sector(s["symbol"])

    # ===== LEADER =====
    leaders = find_sector_leaders(stocks)

    for s in stocks:
        s["is_leader"] = leaders.get(s.get("sector")) == s.get("symbol")

    # ===== MARKET ANALYSIS =====
    market = market_full(stocks)

    # ===== SECTOR TOP =====
    sectors = sector_top(stocks)

    # ===== SNIPER =====
    print("STEP 2: SNIPER")

    sniper = select_sniper(stocks)

    if not sniper:
        print("⚠ No sniper picks")
        return

    print(f"Sniper picks: {len(sniper)}")

    # ===== POSITION =====
    for s in sniper:
        pm = manage_position(s)
        if pm:
            s.update(pm)

    # ===== ENRICH =====
    sniper = [enrich_stock(s) for s in sniper]

    # ===== REPORT =====
    print("STEP 3: REPORT")

    send_report(sniper, market, sectors)

    print("✅ DONE")


if __name__ == "__main__":
    run()
