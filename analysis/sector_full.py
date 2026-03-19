from data.symbol_loader import build_symbol_map

SYMBOL_MAP = build_symbol_map()

def detect_sector(symbol):
    return SYMBOL_MAP.get(symbol, "KHÁC")
    
