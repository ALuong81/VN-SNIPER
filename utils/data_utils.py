def ensure_sector_column(df, default="KHÁC"):
    if "sector" not in df.columns:
        df = df.copy()
        df["sector"] = default
    return df
