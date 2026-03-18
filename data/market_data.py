from vnstock import stock_historical_data
import pandas as pd
import time


def load_stock(symbol):

    for attempt in range(3):

        try:
            df = stock_historical_data(
                symbol=symbol,
                start_date="2024-01-01",
                end_date="2026-12-31",
                resolution="1D"
            )

            # ===== VALIDATE =====
            if df is None or len(df) < 60:
                raise ValueError("Not enough data")

            # ===== CLEAN DATA =====
            df = df.dropna()

            if "close" not in df or "volume" not in df:
                raise ValueError("Missing columns")

            close = pd.Series(df["close"]).astype(float)
            volume = pd.Series(df["volume"]).astype(float)

            if close.isna().all() or volume.isna().all():
                raise ValueError("Invalid series")

            return {
                "symbol": symbol,
                "close": close.reset_index(drop=True),
                "volume": volume.reset_index(drop=True)
            }

        except Exception as e:
            print(f"[LOAD FAIL {attempt+1}] {symbol}")
            time.sleep(0.3)

    return None
