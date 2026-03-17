from analysis.utils import last, mean

def sniper_pro(s):

    close = s["close"]
    volume = s["volume"]

    price = last(close)
    high = float(close.tail(50).max())

    vol = last(volume)
    avg = mean(volume)

    if price < high * 0.95:
        return 0

    if vol < avg * 1.2:
        return 0

    score = 50

    if price >= high:
        score += 20

    if vol > avg * 1.5:
        score += 15

    return score
