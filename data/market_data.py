from vnstock import stock_historical_data

def normalize_price(series):
    # nếu giá > 1000 → chia lại
    if series.max() > 1000:
        return series / 1000
    return series


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

        close = normalize_price(df["close"])
        volume = df["volume"]

        return {
            "symbol": symbol,
            "close": close,
            "volume": volume
        }

    except Exception as e:
        print(f"Load error {symbol}: {e}")
        return None
