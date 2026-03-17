def last(series, default=0.0):
    try:
        return float(series.iloc[-1])
    except:
        return default

def mean(series, n=20):
    try:
        return float(series.tail(n).mean())
    except:
        return 0.0
