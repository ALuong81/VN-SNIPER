from analysis.utils import last


def manage_position(s):

    close = s["close"]

    if len(close) < 20:
        return None

    price = last(close)

    entry = s.get("entry", price)
    sl = s.get("sl", price * 0.93)

    # ===== PROFIT =====
    profit = (price - entry) / entry

    # ===== TRAILING =====
    if profit > 0.15:
        trailing_sl = price * 0.93
        action = "TRAILING STOP - GIỮ LÃI"

    elif profit > 0.08:
        trailing_sl = entry
        action = "DỜI STOP VỀ HÒA VỐN"

    elif profit < -0.05:
        trailing_sl = price
        action = "CẮT LỖ NGAY"

    else:
        trailing_sl = sl
        action = "GIỮ LỆNH"

    return {
        "profit": round(profit * 100, 2),
        "trailing_sl": round(trailing_sl, 2),
        "action": action
    }
