SECTOR_MAP = {
    "VCG": "XÂY DỰNG",
    "HBC": "XÂY DỰNG",
    "VHC": "THỦY SẢN",
    "ANV": "THỦY SẢN",
    "NVL": "BẤT ĐỘNG SẢN",
    "KDH": "BẤT ĐỘNG SẢN",
}

def detect_sector(symbol):
    return SECTOR_MAP.get(symbol, "KHÁC")


def sector_top(stocks):

    score = {}

    for s in stocks:

        sec = s.get("sector", "KHÁC")

        score[sec] = score.get(sec, 0) + s.get("meta_score", 0)

    ranked = sorted(score.items(), key=lambda x: x[1], reverse=True)

    return ranked[:3]
