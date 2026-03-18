import asyncio

from analysis.position_manager import manage_position

from analysis.relative_strength import calc_rs
from analysis.sector_leader import find_sector_leaders

from analysis.market_full import market_full
from analysis.sector_full import detect_sector, sector_top
from analysis.enrich_engine import enrich_stock

from engine.async_scanner_engine import scan_market_async
from analysis.meta_score import score_stock
from analysis.market_engine import analyze_market
from signals.sniper_selector import select_sniper
from risk.engine import apply_risk
from report.telegram_report import send_report


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
    
def run():

    print("STEP 1: SCAN")

    stocks = asyncio.run(scan_market_async())

    if not stocks:
        print("No data")
        return

    # ===== SCORE =====
    for s in stocks:
        s["meta_score"] = score_stock(s)

    # ===== MARKET =====
    market = analyze_market(stocks)

    # ===== market return =====
    market_ret = calc_market_return(stocks)

    # ===== RS =====
    for s in stocks:
        s["rs"] = calc_rs(s, market_ret)

    # ===== leader =====
    leaders = find_sector_leaders(stocks)

    # ===== gắn leader flag =====
    for s in stocks:
        if leaders.get(s["sector"]) == s["symbol"]:
            s["is_leader"] = True
        else:
            s["is_leader"] = False
        
    # ===== FILTER =====
    stocks = [s for s in stocks if s["meta_score"] >= 50]

    # ===== SNIPER =====
    sniper = select_sniper(stocks)

    for s in picks:
        pm = manage_position(s)
        if pm:
            s.update(pm)
        
    # ===== enrich =====
    for s in stocks:
        s["sector"] = detect_sector(s["symbol"])
        s["meta_score"] = score_stock(s)

    # ===== market =====
    market = market_full(stocks)

    # ===== sector =====
    sectors = sector_top(stocks)

    # ===== sniper =====
    sniper = select_sniper(stocks)

    # ===== enrich sniper =====
    sniper = [enrich_stock(s) for s in sniper]

    # ===== REPORT =====
    send_report(sniper, market, sectors)
    


if __name__ == "__main__":
    run()
