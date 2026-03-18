def find_sector_leaders(stocks):

    sector_map = {}

    for s in stocks:

        sec = s.get("sector", "KHÁC")

        if sec not in sector_map:
            sector_map[sec] = []

        sector_map[sec].append(s)

    leaders = {}

    for sec, items in sector_map.items():

        ranked = sorted(
            items,
            key=lambda x: (
                x.get("rs", 0),
                x.get("meta_score", 0)
            ),
            reverse=True
        )

        leaders[sec] = ranked[0]["symbol"]

    return leaders
