from analysis.utils import last, mean


def compute_entry(s):

    close = s["close"]
    volume = s["volume"]

    if len(close) < 60:
        return None

    price = last(close)

    ma20 = last(close.rolling(20).mean())

    high_20 = float(close.tail(20).max())
    low_20 = float(close.tail(20).min())

    vol = last(volume)
    avg_vol = mean(volume, 20)

    # ===== ZONE =====
    pullback_zone = price <= high_20 * 1.02

    # ===== VOLUME =====
    vol_dry = vol < avg_vol * 0.9

    # ===== ENTRY TYPE =====
    if pullback_zone and vol_dry:
        entry_type = "PULLBACK"

        entry = price
        tp = price * 1.2
        sl = ma20 * 0.97

    else:
        entry_type = "BREAKOUT"

        entry = high_20 * 1.01
        tp = entry * 1.15
        sl = low_20 * 0.95

    rr = (tp - entry) / (entry - sl) if (entry - sl) != 0 else 0

    return {
        "entry": round(entry, 2),
        "tp": round(tp, 2),
        "sl": round(sl, 2),
        "rr": round(rr, 2),
        "type": entry_type
    }
