def select_sniper(stocks):

    picks = []

    for s in stocks:

        if s["meta_score"] < 60:
            continue

        entry = compute_entry(s)
        if not entry:
            continue

        if entry["rr"] < 1.8:
            continue

        if not is_valid_breakout(s):
            continue

        s.update(entry)
        s["sniper_score"] = sniper_pro(s)

        if s["sniper_score"] >= 75:
            picks.append(s)

    # fallback nếu không có hàng đẹp
    if not picks:
        print("⚠ No perfect sniper → fallback picks")

        fallback = sorted(stocks, key=lambda x: x["meta_score"], reverse=True)
        return fallback[:2]

    return sorted(picks, key=lambda x: x["sniper_score"], reverse=True)[:5]
