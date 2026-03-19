import os
print(">>> USING symbol_loader:", os.path.abspath(__file__))
import csv

def normalize(symbol):
    return symbol.strip().upper()


def load_symbols():

    symbols = []
    sector_map = {}

    with open("data/full_symbols.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:

            symbol = normalize(row.get("symbol", ""))

            sector = (
                row.get("sector")
                or row.get("secter")
                or row.get("Sector")
                or "KHÁC"
            ).strip().upper()

            if symbol:
                symbols.append(symbol)
                sector_map[symbol] = sector

    return symbols, sector_map
