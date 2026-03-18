from analysis.sniper_pro import sniper_pro
from analysis.breakout_filter import is_valid_breakout
from analysis.entry_engine import compute_entry


def select_sniper(stocks):

    picks = []
    fallback = []

    for s in stocks:

        # ===== SCORE =====
        s["sniper_score"] = sniper_pro(s)

        # ===== BREAKOUT CHECK =====
        valid_breakout = is_valid_breakout(s)
        s["breakout_quality"] = "CHUẨN" if valid_breakout else "NGHI NGỜ"

        # ===== ENTRY =====
        entry_data = compute_entry(s)

        if entry_data:
            s.update(entry_data)
        else:
            # fallback entry (để không mất dữ liệu)
            s["entry"] = s.get("close").iloc[-1]
            s["tp"] = s["entry"] * 1.1
            s["sl"] = s["entry"] * 0.95
            s["rr"] = (s["tp"] - s["entry"]) / (s["entry"] - s["sl"])

        # ===== PHÂN LOẠI =====
        if s["sniper_score"] >= 70 and s["rr"] >= 1.5 and valid_breakout:
            s["status"] = "ĐẸP"
            picks.append(s)

        elif s["sniper_score"] >= 60:
            s["status"] = "THEO DÕI"
            fallback.append(s)

        else:
            continue

    # ===== ƯU TIÊN KÈO ĐẸP =====
    if picks:
        return sorted(picks, key=lambda x: x["sniper_score"], reverse=True)[:5]

    # ===== KHÔNG CÓ → LẤY KÈO THEO DÕI =====
    if fallback:
        print("⚠ No perfect sniper → fallback picks")
        return sorted(fallback, key=lambda x: x["sniper_score"], reverse=True)[:5]

    # ===== STILL NOTHING → LẤY TOP META =====
    print("⚠ No sniper at all → emergency fallback")

    return sorted(
        stocks,
        key=lambda x: x.get("meta_score", 0),
        reverse=True
    )[:3]
