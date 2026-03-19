def sector_top(stocks):

    sector_score = {}

    for s in stocks:
        sector = s.get("sector", "KHÁC")

        score = s.get("meta_score", 0)

        sector_score.setdefault(sector, []).append(score)

    result = []

    for k, v in sector_score.items():
        avg = sum(v) / len(v)
        result.append((k, round(avg, 2)))

    result.sort(key=lambda x: x[1], reverse=True)

    return result[:3]
