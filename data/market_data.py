from vnstock import stock_historical_data
import os
print(">>> USING market_data:", os.path.abspath(__file__))

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

        if len(df) < 60:
            return None

        return {
            "symbol": symbol,
            "close": df["close"],
            "volume": df["volume"]
        }

    except Exception as e:
        print(f"Load error: {symbol}")
        return None
