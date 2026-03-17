from vnstock import stock_historical_data
from analysis.utils import last

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

        return {
            "symbol": symbol,
            "close": df["close"],
            "volume": df["volume"]
        }

    except:
        return None
