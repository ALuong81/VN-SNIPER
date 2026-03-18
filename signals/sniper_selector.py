from analysis.sniper_pro import sniper_pro
from analysis.breakout_filter import is_valid_breakout


def select_sniper(stocks):

    picks = []

    for s in stocks:

        s["sniper_score"] = sniper_pro(s)

        # 🚨 FILTER QUAN TRỌNG
        if not is_valid_breakout(s):
            continue

        if s["sniper_score"] >= 70:
            picks.append(s)

    return sorted(picks, key=lambda x: x["sniper_score"], reverse=True)[:5]
