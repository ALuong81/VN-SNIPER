from analysis.sniper_pro import sniper_pro
from analysis.breakout_filter import is_valid_breakout
from analysis.entry_engine import compute_entry


def select_sniper(stocks):

    picks = []

    for s in stocks:

        s["sniper_score"] = sniper_pro(s)

        entry_data = compute_entry(s)

        if not entry_data:
            continue

        s.update(entry_data)

        # 🔥 LỌC CHẶT
        if not is_valid_breakout(s):
            continue

        if entry_data["rr"] < 1.5:
            continue

        if s["sniper_score"] >= 70:
            picks.append(s)

    # ⚠ FALLBACK nếu không có
    if not picks:
        print("⚠ No perfect sniper → fallback picks")

        fallback = sorted(
            stocks,
            key=lambda x: x.get("meta_score", 0),
            reverse=True
        )

        return fallback[:3]

    return sorted(picks, key=lambda x: x["sniper_score"], reverse=True)[:5]
