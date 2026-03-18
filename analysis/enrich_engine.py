from analysis.utils import last, mean
from analysis.breakout_filter import is_valid_breakout

def enrich_stock(s):

    close = s["close"]
    volume = s["volume"]

    price = last(close)
    ma20 = last(close.rolling(20).mean())
    ma50 = last(close.rolling(50).mean())

    vol = last(volume)
    avg = mean(volume)

    # ===== TREND =====
    if price > ma20 > ma50:
        trend = "ĐỒNG THUẬN MẠNH"
    elif price > ma20:
        trend = "ĐỒNG THUẬN"
    else:
        trend = "YẾU"

    # ===== BREAKOUT =====
    high = float(close.tail(50).max())

    if price >= high:
        breakout = "XÁC SUẤT CAO"
    else:
        breakout = "THẤP"

    # ===== FLOW =====
    if vol > avg * 1.5:
        flow = "MẠNH"
    elif vol > avg:
        flow = "TRUNG BÌNH"
    else:
        flow = "YẾU"
valid = is_valid_breakout(s)

s["entry_type"] = s.get("type", "UNKNOWN")

if s.get("rr", 0) > 2:
    s["entry_quality"] = "RẤT ĐẸP"
elif s.get("rr", 0) > 1.5:
    s["entry_quality"] = "ỔN"
else:
    s["entry_quality"] = "KÉM"
    
    s.update({
        "trend_multi_tf": trend,
        "breakout_prob": breakout,
        "smart_money": flow,
        "whale": "DÒNG TIỀN LỚN" if vol > avg * 1.5 else "BÌNH THƯỜNG",
        "ai_pattern": "BREAKOUT PATTERN" if price >= high else "NO PATTERN",
        "vcp": "KHÔNG",
        "supply": "BÌNH THƯỜNG",
        "super_breakout": "THẤP",
        "early_breakout": "KHÔNG",
        "super_stock": "TIỀM NĂNG" if s["meta_score"] > 80 else "BÌNH THƯỜNG",
        "rank": "SIÊU MẠNH" if s["meta_score"] > 80 else "MẠNH",
        "rs": "SIÊU MẠNH" if s.get("rs", 0) > 0 else "YẾU",
        "leader" = "CÓ" if s.get("is_leader") else "KHÔNG",
        "breakout_quality" = "CHUẨN" if valid else "NGHI NGỜ",
        "risk": "BÌNH THƯỜNG"
    })

s["action"] = s.get("action", "CHỜ")
s["profit"] = s.get("profit", 0)
s["trailing_sl"] = s.get("trailing_sl", 0)

    return s
