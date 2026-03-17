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

    if price > ma20: score += 20
    if price > ma50: score += 20
    if vol > avg: score += 20

    if price >= float(close.tail(50).max()):
        score += 30

    return score
