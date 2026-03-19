import pandas as pd
import requests

def is_valid_symbol(symbol: str) -> bool:
    """
    Kiểm tra symbol hợp lệ bằng API hoặc danh sách whitelist.
    Trả về True nếu hợp lệ, False nếu invalid.
    """
    # Ví dụ dùng API check, replace bằng endpoint thật
    url = f"https://api.example.com/validate_symbol/{symbol}"
    try:
        r = requests.get(url, timeout=3)
        return r.status_code == 200 and r.json().get("valid", False)
    except:
        return False

def load_symbols(limit=None):
    """
    Load symbol từ CSV/DB, lọc symbol invalid.
    """
    df = pd.read_csv("data/symbols.csv")
    
    # Lọc symbol invalid
    df['valid'] = df['symbol'].apply(is_valid_symbol)
    df = df[df['valid']]
    
    if limit:
        df = df.head(limit)
    
    return df[['symbol', 'exchange', 'sector']]
    