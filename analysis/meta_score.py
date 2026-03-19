from analysis.utils import last, mean


def score_stock(s):

    close = s["close"]
    volume = s["volume"]

    price = last(close)
    ma20 = last(close.rolling(20).mean())
    ma50 = last(close.rolling(50).mean())

    vol = last(volume)
    avg = mean(volume)

    score = 0

    # ===== TREND =====
    if price > ma20 > ma50:
        score += 30
    elif price > ma20:
        score += 15

    # ===== BREAKOUT =====
    if price >= float(close.tail(50).max()):
        score += 25

    # ===== VOLUME =====
    if vol > avg * 1.2:
        score += 20

    # ===== RELATIVE STRENGTH =====
    rs = s.get("rs", 0)

    if rs > 0:
        score += 15
    else:
        score -= 20   # 🚨 cực quan trọng

    # ===== LEADER =====
    if s.get("is_leader"):
        score += 10

    # ===== PENALTY SIDEWAY =====
    if abs(price - ma20) / ma20 < 0.02:
        score -= 10

    # ===== CLAMP =====
    score = max(0, min(100, score))

    return score
