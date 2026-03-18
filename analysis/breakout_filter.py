from analysis.utils import last, mean


def is_valid_breakout(s):

    close = s["close"]
    volume = s["volume"]

    if len(close) < 60:
        return False

    price = last(close)
    prev_price = close.iloc[-2]

    high_50 = float(close.tail(50).max())

    vol = last(volume)
    avg_vol = mean(volume, 20)

    # ===== 1. BREAKOUT =====
    breakout = price >= high_50 * 0.98

    # ===== 2. VOLUME CONFIRM =====
    vol_ok = vol > avg_vol * 1.3

    # ===== 3. KHÔNG BỊ ĐẠP NGƯỢC =====
    change = (price - prev_price) / prev_price

    no_fake_dump = change > -0.02

    # ===== 4. FOLLOW-THROUGH =====
    prev_high = float(close.iloc[-2:-1].max())

    follow = price >= prev_high

    return breakout and vol_ok and no_fake_dump and follow
