from .dataset import LOW_PRICE_CORPUS, MEDIUM_PRICE_CORPUS, HIGH_PRICE_CORPUS

def query_type(df, type):
    df = df[df["type"].str.contains(type)]
    return df

def query_price(df, price):
    if price in LOW_PRICE_CORPUS:
        price_symbol = "฿"
    elif price in MEDIUM_PRICE_CORPUS:
        price_symbol = "฿฿"
    elif price in HIGH_PRICE_CORPUS:
        price_symbol = "฿฿฿"

    df = df[df["price"] == price_symbol]
    return df

def query_in_period_time(df, select_time):
    df = df[
        (df["opening time"] <= select_time) & (select_time <= df["closing time"])]
    return df
