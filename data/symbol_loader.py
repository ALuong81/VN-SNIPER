import pandas as pd

def load_symbol_data():

    df = pd.read_csv("data/full_symbols.csv")

    df.columns = [c.lower().strip() for c in df.columns]

    df = df.rename(columns={
        "secter": "sector"  # fix typo
    })

    return df


def build_symbol_map():

    df = load_symbol_data()

    return {
        row["symbol"]: row["sector"]
        for _, row in df.iterrows()
    }
