import csv


def load_symbols():

    symbols = []

    try:
        with open("data/full_symbols.csv", newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:

                symbol = row.get("symbol", "").strip().upper()
                exchange = row.get("exchange", "").strip().upper()
                sector = row.get("sector", "KHÁC").strip().upper()

                # 🚨 FILTER CỨNG
                if not symbol:
                    continue

                if len(symbol) > 5:   # loại mã rác
                    continue

                if exchange not in ["HOSE", "HNX", "UPCOM"]:
                    continue

                symbols.append({
                    "symbol": symbol,
                    "exchange": exchange,
                    "sector": sector
                })

    except Exception as e:
        print("Load symbols error:", e)
        return []

    print(f"Universe loaded: {len(symbols)}")

    return symbols
