import pandas as pd
import requests

VNSTOCK_API = "https://finfo-api.vndirect.com.vn/v4/quotes"  # API công khai VNStock

def get_close_price(symbol: str):
    """
    Lấy giá đóng cửa hiện tại của một cổ phiếu từ VNStock.
    """
    try:
        r = requests.get(VNSTOCK_API, params={"symbols": symbol})
        data = r.json()
        # VNStock trả về list của symbol
        if "data" in data and len(data["data"]) > 0:
            return data["data"][0].get("close", 0.0)
        return 0.0
    except Exception:
        return 0.0

def load_symbols(limit=None):
    """
    Load danh sách symbol + exchange + sector + close price từ full_symbols.csv
    """
    try:
        df = pd.read_csv("data/full_symbols.csv")
    except FileNotFoundError:
        raise FileNotFoundError("File data/full_symbols.csv không tìm thấy!")

    # fallback nếu thiếu cột
    if 'sector' not in df.columns:
        df['sector'] = 'KHÁC'
    if 'exchange' not in df.columns:
        df['exchange'] = 'VN'

    # Lấy giá close từ VNStock
    df['close'] = df['symbol'].apply(get_close_price)

    if limit is not None:
        df = df.head(limit)

    return df[['symbol', 'exchange', 'sector', 'close']]
