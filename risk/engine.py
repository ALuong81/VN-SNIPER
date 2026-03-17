from analysis.utils import last

def apply_risk(s):

    price = last(s["close"])

    s["entry"] = price
    s["target"] = round(price * 1.2, 2)
    s["stop"] = round(price * 0.93, 2)

    return s
