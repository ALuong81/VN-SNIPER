def analyze_market(stocks):

    up = sum(1 for s in stocks if s["close"].iloc[-1] > s["close"].iloc[-2])
    ratio = round(up / len(stocks) * 100, 1)

    if ratio < 40:
        return {"status": "RỦI RO", "trend": "GIẢM"}
    elif ratio < 60:
        return {"status": "TRUNG LẬP", "trend": "SIDEWAY"}
    else:
        return {"status": "TỐT", "trend": "TĂNG"}
