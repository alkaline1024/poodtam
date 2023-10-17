from .dataset import LOW_PRICE_CORPUS, MEDIUM_PRICE_CORPUS, HIGH_PRICE_CORPUS, BREAKFAST_CORPUS, LUNCH_CORPUS, DINNER_CORPUS, NOW_TIME_CORPUS
import datetime

def query_type(df, type):
    df = df[df["type"].str.contains(type)]
    return df

def query_price(df, price):
    print(price)

    price_symbol = None
    if price in LOW_PRICE_CORPUS:
        price_symbol = "฿"
    elif price in MEDIUM_PRICE_CORPUS:
        price_symbol = "฿฿"
    elif price in HIGH_PRICE_CORPUS:
        price_symbol = "฿฿฿"

    if price_symbol:
        df = df[df["price"] == price_symbol]
    return df

def query_in_period_time(df, chat):
    current_time = chat.current_time
    if current_time in BREAKFAST_CORPUS:
        print("BREAKFAST_CORPUS")
        queried_df = df[(df["opening time"] < datetime.time(12))]
    elif current_time in LUNCH_CORPUS:
        print("LUNCH_CORPUS")
        queried_df = df[(df["opening time"] < datetime.time(16))]
    elif current_time in DINNER_CORPUS:
        print("DINNER_CORPUS")
        queried_df = df[(df["opening time"] < datetime.time(23))]
    elif current_time in NOW_TIME_CORPUS:
        queried_df = query_in_period_now(df)
    else:
        selected_time = chat.selected_time.time()
        queried_df = df[(df["opening time"] <= selected_time) & (selected_time <= df["closing time"])]
    return queried_df

def query_in_period_now(df):
    current_time = datetime.datetime.now().time()
    df = df[(df["opening time"] <= current_time) & (current_time <= df["closing time"])]
    return df
