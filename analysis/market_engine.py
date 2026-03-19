def analyze_market(stocks):

    up = 0
    total = 0

    for s in stocks:
        try:
            c = s["close"]

            if len(c) < 2:
                continue

            if c.iloc[-1] > c.iloc[-2]:
                up += 1

            total += 1

        except:
            continue

    breadth = round(up / total * 100, 2) if total else 0

    # ===== TREND =====
    if breadth > 60:
        trend = "TĂNG"
        status = "TỐT"
    elif breadth > 40:
        trend = "TRUNG TÍNH"
        status = "BÌNH THƯỜNG"
    else:
        trend = "GIẢM"
        status = "RỦI RO"

    return {
        "breadth": breadth,
        "trend": trend,
        "status": status,
        "momentum": "Uptrend" if trend == "TĂNG" else "Sideway"
    }
