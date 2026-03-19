from analysis.utils import last, mean


def compute_entry(s):

    close = s["close"]
    volume = s["volume"]

    if len(close) < 60:
        return None

    price = last(close)

    ma20 = last(close.rolling(20).mean())
    ma50 = last(close.rolling(50).mean())

    high_20 = float(close.tail(20).max())
    low_20 = float(close.tail(20).min())

    vol = last(volume)
    avg_vol = mean(volume, 20)

    # ===== BREAKOUT VALIDATION =====
    breakout = price >= high_20 * 0.98

    # ===== VOLUME CONFIRM =====
    vol_confirm = vol > avg_vol * 1.2

    # ===== ENTRY =====
    if breakout and vol_confirm:
        entry_type = "BREAKOUT"

        entry = high_20 * 1.01
        sl = ma20 * 0.98

    else:
        # Pullback only nếu trend đẹp
        if not (price > ma20 > ma50):
            return None

        entry_type = "PULLBACK"

        entry = price
        sl = ma50 * 0.97

    # ===== TP DYNAMIC =====
    risk = entry - sl

    if risk <= 0:
        return None

    tp = entry + risk * 2   # RR = 2 chuẩn

    rr = (tp - entry) / risk

    # ===== FILTER KÈO XẤU =====
    if rr < 1.5:
        return None

    return {
        "entry": round(entry, 2),
        "tp": round(tp, 2),
        "sl": round(sl, 2),
        "rr": round(rr, 2),
        "type": entry_type
    }
