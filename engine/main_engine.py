import asyncio

from engine.async_scanner_engine import scan_market_async
from analysis.meta_score import score_stock
from analysis.market_engine import analyze_market
from analysis.sector_full import sector_top
from signals.sniper_selector import select_sniper
from analysis.enrich_engine import enrich_stock

import pandas as pd

df = pd.read_csv("data/full_symbols.csv")
print("COLUMNS:", df.columns.tolist())

def run():

    print("STEP 1: SCAN")

    stocks, sector_map = asyncio.run(scan_market_async())

    print(f"Loaded: {len(stocks)}")

    # đảm bảo không crash
    sector_map = sector_map or {}

    # ===== GẮN SECTOR =====
    
    for s in stocks:
        symbol = s["symbol"]
        s["sector"] = sector_map.get(symbol, "KHÁC")

    if not stocks:
        print("No data")
        return

    print(f"Loaded: {len(stocks)}")

    # ===== SCORE =====
    for s in stocks:
        s["meta_score"] = score_stock(s)

    # ===== FILTER =====
    stocks = [s for s in stocks if s["meta_score"] >= 40]

    if not stocks:
        print("❌ No stocks after score filter")
        return

    # ===== MARKET =====
    market = analyze_market(stocks)

    # ===== SNIPER =====
    print("STEP 2: SNIPER")

    sniper = select_sniper(stocks)

    if not sniper:
        print("⚠ No sniper picks")
        return

    print(f"Sniper picks: {len(sniper)}")

    # ===== ENRICH =====
    sniper = [enrich_stock(s) for s in sniper]

    # ===== SECTOR =====
    sectors = sector_top(stocks)

    # ===== REPORT =====
    print("\nSTEP 3: REPORT\n")

    print(f"📈 Trạng thái thị trường: {market['status']}")
    print(f"📊 Xu hướng thị trường: {market['trend']}")
    print(f"⏱ Nhịp thị trường: {market['momentum']}")
    print(f"• Độ rộng thị trường: {'Rộng' if market['breadth'] > 60 else 'Hẹp'}")
    print(f"• Tỷ lệ cổ phiếu tăng: {market['breadth']}%\n")

    print("🔥 TOP NGÀNH MẠNH")
    for i, (name, score) in enumerate(sectors, 1):
        print(f"{i}. {name} ({score})")

    print("\n------------------------------------\n")

    for i, s in enumerate(sniper, 1):

        price = float(s["close"].iloc[-1])

        print(f"🔹 Mục tiêu #{i}: {s['symbol']}\n")

        print(f"• Giá hiện tại: {round(price,2)}")
        print(f"• Giá vào dự kiến: {s['entry']}")
        print(f"• Mục tiêu chốt lời: {s['tp']}")
        print(f"• Cắt lỗ: {s['sl']}")
        print(f"• Ngành: {s['sector']}")
        print(f"• Xu hướng đa khung: {s['trend_multi_tf']}")
        print(f"• Khả năng bứt phá: {s['breakout_prob']}")
        print(f"• Meta Score: {s['meta_score']}")
        print()

    print("✅ DONE")


if __name__ == "__main__":
    run()
