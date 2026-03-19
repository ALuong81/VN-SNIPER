#full_symbols
# data/symbol_loader.py

import pandas as pd

def load_symbols(limit=None):
    """
    Load danh sách symbol từ file CSV.
    
    Tham số:
        limit (int, optional): số lượng symbol muốn lấy. Mặc định None = lấy tất cả.
    
    Trả về:
        DataFrame gồm các cột: ['symbol', 'exchange', 'sector']
    """
    try:
        df = pd.read_csv("data/full_symbols.csv")
    except FileNotFoundError:
        raise FileNotFoundError("File data/full_symbols.csv không tìm thấy!")

    # Nếu không có cột sector thì fallback = KHÁC
    if 'sector' not in df.columns:
        df['sector'] = 'KHÁC'

    # Giới hạn số lượng nếu có tham số limit
    if limit is not None:
        df = df.head(limit)

    # Chỉ trả về 3 cột cần thiết
    return df[['symbol', 'exchange', 'sector']]
