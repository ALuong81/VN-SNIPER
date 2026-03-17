import asyncio

from engine.async_scanner_engine import scan_market_async
from analysis.meta_score import score_stock
from analysis.market_engine import analyze_market
from signals.sniper_selector import select_sniper
from risk.engine import apply_risk
from report.telegram_report import send_report


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

    # ===== FILTER =====
    stocks = [s for s in stocks if s["meta_score"] >= 50]

    # ===== SNIPER =====
    sniper = select_sniper(stocks)

    # ===== RISK =====
    sniper = [apply_risk(s) for s in sniper]

    # ===== REPORT =====
    send_report(sniper, market)


if __name__ == "__main__":
    run()
