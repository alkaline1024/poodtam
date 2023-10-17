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
df_types = df["type"].str.split(",").tolist()
restaurant_types = list(set([word for sublist in df_types for word in sublist]))
restaurant_types.sort()
TYPE_CORPUS = restaurant_types
TYPE_CHOICES_HTML = '<div class="ui labels">' + ' '.join([f'<a class="ui teal label"' + ' onclick=' + '"' + f"console.log('hello, world!'); input=$('#input')[0]; input.value+='{type} '; input.focus()" + '">' + type + '</a>' for type in TYPE_CORPUS]) + '</div>'

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
    "฿",
    "lowest price",
    "low",
    "lower",
    "less",
    "min",
    "minimun price",
    "less than 100 baht",
]
MEDIUM_PRICE_CORPUS = [
    "฿฿",
    "medium price",
    "medium",
    "average",
    "normal price",
    "normal",
    "betweem 100 baht and 250 baht",
]
HIGH_PRICE_CORPUS = [
    "฿฿฿",
    "highest price",
    "higher",
    "high",
    "maximum price",
    "max",
    "more than 250 baht",
]
PRICE_CORPUS = (
    LOW_PRICE_CORPUS + MEDIUM_PRICE_CORPUS + HIGH_PRICE_CORPUS + ANYPRICE_CORPUS
)

# *** TIME DATASET ***
ANYTIME_CORPUS = [
    "anytime",
    "alltime",
    "allday",
    "all day",
    "everytime",
    "not specific",
]
NOW_TIME_CORPUS = [
    "now",
    "currently",
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
    "specific",
    "time"
]
BREAKFAST_CORPUS = [
    "breakfast",
    "morning",
]
LUNCH_CORPUS = [
    "lunch",
    "noon",
]
DINNER_CORPUS = [
    "afternoon",
    "dinner",
    "night",
    "midnight",
]
CHOOSE_TIME_CORPUS = NOW_TIME_CORPUS + BREAKFAST_CORPUS + LUNCH_CORPUS + DINNER_CORPUS
TIME_CORPUS = CHOOSE_TIME_CORPUS + ANYTIME_CORPUS + SPECIFIC_TIME_CORPUS

RESET_CORPUS = [
    "reset",
    "restart",
    "again",
]

# *** COMBINED DATASET ***
ALL_CORPUS = GREETING_CORPUS + TYPE_CORPUS + PRICE_CORPUS + TIME_CORPUS

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

UNNECESSARY_WORDS = [
    ",",
    ".",
    "!",
    "and",
    "restaurants",
    "restaurant",
    "stores",
    "store",
    "shops"
    "shop",
    "food",
    "please",
    "give",
    "me",
    "my",
    "mine",
    "a",
    "i",
    "to",
    "in",
    "want",
    "some",
    "can",
    "you",
    "just",
    "for",
    "but",
    "type",
    "best",
    "good",
    "with",
    "price",
    "prices",
    "the",
    "that",
    "thad",
    "dat",
    "you",
    "u",
    "have",
]
