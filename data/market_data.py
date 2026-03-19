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

        # 🚨 FIX SCALE GIÁ
        if df["close"].max() > 1000:
            df["close"] = df["close"] / 1000

        return {
            "symbol": symbol,
            "close": df["close"],
            "volume": df["volume"]
        }

    except Exception as e:
        print(f"❌ {symbol}: {e}")
        return None
