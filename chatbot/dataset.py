import pandas as pd

df = pd.read_excel("chatbot/csv/Hatyai_restaurant.xlsx")

GREETING_CORPUS = [
    "เอาใหม่",
    "สวัสดี",
    "สวัสดีค่ะ",
    "สวัสดีครับ",
    "สวัสดีคับ",
    "สวัสดีงับ",
    "ว่าไง",
    "หืมมม...",
    "ดี",
    "ดีจ้า",
    "ไง",
    "โย่ว",
    "hello",
    "hi",
    "hey",
    "hola",
    "good morning",
    "good afternoon",
    "what sup",
    "what's up",
]

# *** TYPE DATASET ***
df_types = df["type"].str.split(", ").tolist()
restaurant_types = list(set([word for sublist in df_types for word in sublist]))
restaurant_types.sort()
TYPE_CORPUS = restaurant_types

# *** PRICE DATASET ***
PRICE_CHOICES = [
    ("฿", "฿ (less than 100 baht)"),
    ("฿฿", "฿฿ (100 baht- 250 baht)"),
    ("฿฿฿", "฿฿฿ (more than 250 baht)")
]
ANYPRICE_CORPUS = [
    "all",
    "all price",
    "anyprice",
    "any price",
    "any",
    "every price",
    "not specific",
]
LOW_PRICE_CORPUS = [
    "lowest price",
    "low",
    "lower",
    "less",
    "min",
    "minimun price",
    "less than 100 baht",
]
MEDIUM_PRICE_CORPUS = [
    "medium price",
    "medium",
    "average",
    "normal price",
    "normal",
    "betweem 100 baht and 250 baht",
]
HIGH_PRICE_CORPUS = [
    "highest price",
    "higher",
    "high",
    "maximum price",
    "max",
    "more than 250 baht",
]
PRICE_RANGE_CORPUS = (
    LOW_PRICE_CORPUS + MEDIUM_PRICE_CORPUS + HIGH_PRICE_CORPUS + ANYPRICE_CORPUS
)

# *** TIME DATASET ***
ANYTIME_CORPUS = [
    "any time",
    "anytime",
    "alltime",
    "allday",
    "all day",
    "everytime",
    "not specific",
]
SPECIFIC_TIME_CORPUS = [
    "select",
    "select time",
    "choose",
    "i'll choose",
    "ill choose",
    "i will choose",
    "choose myself",
    "myself",
]
TIME_CORPUS = ANYTIME_CORPUS + SPECIFIC_TIME_CORPUS


RESET_CORPUS = [
    "reset",
    "restart",
    "again",
]

# *** COMBINED DATASET ***
ALL_CORPUS = GREETING_CORPUS + TYPE_CORPUS + PRICE_RANGE_CORPUS + TIME_CORPUS

# *** BOT ANSWER DATASET ***
GREETING_CHOICE = ["Hey ", "Hello ", "Hi " "What's up ", "Greeting "]
ACCEPTED_CHOICE = ["Alright", "Got it", "Got it", "Roger that", "Yes, sir"]
SAD_EMOJI_CHOICE = [";-;", ";--;", ";---;", ";___;", ";_;", ";^;", ":(", "(;__;)", "(._.)"]
HAPPY_EMOJI_CHOICE = ["! ", ". ", ". ^ ^ ", " :D ", "! :) ", "! :D ", ":3 ", "<3 ", "\o/ "]
RECOMMAND_CHOICE = ["What kind of restaurant would you like me to recommend?","What kind of restaurant do you like?",]

LABEL_COLORS = [
    "orange",
    "yellow",
    "olive",
    "green",
    "teal",
    "blue",
    "violet",
    "purple",
    "pink",
    "brown",
]