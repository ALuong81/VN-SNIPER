import pandas as pd

def ensure_sector_column(df):
    df = df.copy()
    df['sector'] = df.get('sector', 'KHAC')
    df['sector'] = df['sector'].fillna('KHAC')
    return df

def load_symbols(limit=200):

    try:
        df = pd.read_csv("data/full_symbols.csv")

        df = ensure_sector_column(df)
        
        df = df.dropna(subset=["symbol"])

        symbols = df["symbol"].astype(str).str.strip().tolist()

        print(f"Universe loaded: {len(symbols)}")

        return symbols[:limit]

    except Exception as e:
        print(f"❌ Load symbols error: {e}")
        return []
