from analysis.utils import last

def calc_rs(stock, market_avg):

    try:
        price = stock["close"]

        stock_return = (price.iloc[-1] - price.iloc[-20]) / price.iloc[-20]
        market_return = market_avg

        rs = stock_return - market_return

        return round(rs, 4)

    except:
        return 0
