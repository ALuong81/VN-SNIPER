import os
print(">>> USING market_data:", os.path.abspath(__file__))
from vnstock import stock_historical_data

def load_stock(symbol):

    try:
        df = stock_historical_data(
            symbol=symbol,
            start_date="2024-01-01",
            end_date="2026-12-31",
            resolution="1D"
        )

        if df is None or len(df) < 60:
            return None

        df = df.dropna()

        # 🔥 FIX GIÁ (QUAN TRỌNG NHẤT)
        df["close"] = df["close"].astype(float) / 1000

        return {
            "symbol": symbol.strip().upper(),
            "close": df["close"],
            "volume": df["volume"]
        }

    except Exception as e:
        print(f"Load error: {symbol}")
        return None
