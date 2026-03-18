from analysis.sniper_pro import sniper_pro
from analysis.breakout_filter import is_valid_breakout
from analysis.entry_engine import compute_entry


def select_sniper(stocks):

    picks = []

    for s in stocks:

        s["sniper_score"] = sniper_pro(s)

        if not is_valid_breakout(s):
            continue

        entry_data = compute_entry(s)

        if not entry_data:
            continue

        # 🚨 CHỈ GIỮ LỆNH ĐẸP
        if entry_data["rr"] < 1.5:
            continue

        s.update(entry_data)

        if s["sniper_score"] >= 70:
            picks.append(s)

    return sorted(picks, key=lambda x: x["sniper_score"], reverse=True)[:5]
