def market_full(stocks):

    up = 0

    for s in stocks:
        if s["close"].iloc[-1] > s["close"].iloc[-2]:
            up += 1

    total = len(stocks)
    ratio = round(up / total * 100, 1) if total > 0 else 0

    if ratio < 40:
        return {
            "status": "RỦI RO",
            "trend": "GIẢM",
            "timing": "Thị trường điều chỉnh",
            "breadth": "Hẹp",
            "ratio": ratio
        }

    elif ratio < 60:
        return {
            "status": "TRUNG LẬP",
            "trend": "SIDEWAY",
            "timing": "Tích lũy",
            "breadth": "Trung bình",
            "ratio": ratio
        }

    else:
        return {
            "status": "TỐT",
            "trend": "TĂNG",
            "timing": "Uptrend",
            "breadth": "Rộng",
            "ratio": ratio
        }
