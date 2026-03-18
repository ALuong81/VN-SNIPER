from analysis.utils import last, mean
from analysis.breakout_filter import is_valid_breakout


def enrich_stock(s):

    if not s or "close" not in s or "volume" not in s:
        return None

    close = s["close"]
    volume = s["volume"]

    price = last(close)
    ma20 = last(close.rolling(20).mean())
    ma50 = last(close.rolling(50).mean())

    vol = last(volume)
    avg = mean(volume)

    if price is None or ma20 is None or ma50 is None:
        return None
        
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

    # ===== VALID BREAKOUT =====
    valid = is_valid_breakout(s)

    # ===== UPDATE =====
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
        "super_stock": "TIỀM NĂNG" if s.get("meta_score", 0) > 80 else "BÌNH THƯỜNG",
        "rank": "SIÊU MẠNH" if s.get("meta_score", 0) > 80 else "MẠNH",
        "rs": "SIÊU MẠNH" if s.get("rs", 0) > 0 else "YẾU",
        "leader": "CÓ" if s.get("is_leader") else "KHÔNG",
        "breakout_quality": "CHUẨN" if valid else "NGHI NGỜ",
        "entry_type": s.get("type", "UNKNOWN"),
        "action": s.get("action", "CHỜ"),
        "profit": s.get("profit", 0),
        "trailing_sl": s.get("trailing_sl", 0),
        "risk": "BÌNH THƯỜNG"
    })

    # ===== ENTRY QUALITY =====
    rr = s.get("rr", 0)

    if rr > 2:
        s["entry_quality"] = "RẤT ĐẸP"
    elif rr > 1.5:
        s["entry_quality"] = "ỔN"
    else:
        s["entry_quality"] = "KÉM"

    return s
    
