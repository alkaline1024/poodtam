import pandas as pd

df = pd.read_excel("chatbot/csv/Hatyai_restaurant.xlsx")

LABEL_COLORS = ["orange","yellow","olive","green","teal","blue","violet","purple","pink","brown",]

# *** GREETING DATASET ***
GREETING_CORPUS = ["เอาใหม่","สวัสดี","สวัสดีค่ะ","สวัสดีครับ","สวัสดีคับ","สวัสดีงับ","ว่าไง","หืมมม...","ดี","ดีจ้า","ไง","โย่ว","hello","hi","hey","hola","good morning","good afternoon","what sup","what's up",]

# *** TYPE DATASET ***
df_types = df["type"].str.split(",").tolist()
restaurant_types = list(set([word for sublist in df_types for word in sublist]))
restaurant_types.sort()
TYPE_CORPUS = restaurant_types
TYPE_CHOICES_HTML = '<div class="ui labels">' + ' '.join([f'<a class="ui teal label"' + ' onclick=' + '"' + f"console.log('hello, world!'); input=$('#input')[0]; input.value+='{type} '; input.focus()" + '">' + type + '</a>' for type in TYPE_CORPUS]) + '</div>'

# *** PRICE DATASET ***
PRICE_CHOICES = [("฿", "฿ (less than 100 baht)"),("฿฿", "฿฿ (100 baht- 250 baht)"),("฿฿฿", "฿฿฿ (more than 250 baht)")]
ANYPRICE_CORPUS = ["all","all price","anyprice","any price","any","every price","not specific",]
LOW_PRICE_CORPUS = ["฿","lowest price","low","lower","less","min","minimun price","less than 100 baht",]
MEDIUM_PRICE_CORPUS = ["฿฿","medium price","medium","average","normal price","normal","betweem 100 baht and 250 baht",]
HIGH_PRICE_CORPUS = ["฿฿฿","highest price","higher","high","maximum price","max","more than 250 baht",]
PRICE_CORPUS = (LOW_PRICE_CORPUS + MEDIUM_PRICE_CORPUS + HIGH_PRICE_CORPUS + ANYPRICE_CORPUS)

# *** TIME DATASET ***
ANYTIME_CORPUS = ["anytime","alltime","allday","all day","everytime","not specific",]
NOW_TIME_CORPUS = ["now","currently","today",]
SPECIFIC_TIME_CORPUS = ["select","select time","choose","i'll choose","ill choose","i will choose","choose myself","myself","specific","time"]
BREAKFAST_CORPUS = ["breakfast","morning",]
LUNCH_CORPUS = ["lunch","noon",]
DINNER_CORPUS = ["afternoon","dinner","night","midnight",]
CHOOSE_TIME_CORPUS = NOW_TIME_CORPUS + BREAKFAST_CORPUS + LUNCH_CORPUS + DINNER_CORPUS
TIME_CORPUS = CHOOSE_TIME_CORPUS + ANYTIME_CORPUS + SPECIFIC_TIME_CORPUS

RESET_CORPUS = ["reset","restart","again",]

# *** COMBINED DATASET ***
ALL_CORPUS = GREETING_CORPUS + TYPE_CORPUS + PRICE_CORPUS + TIME_CORPUS

# *** BOT ANSWER DATASET ***
GREETING_CHOICE = ["Hey ", "Hello ", "Hi " "What's up ", "Greeting "]
ACCEPTED_CHOICE = ["Alright", "Got it", "Got it", "Roger that", "Yes, sir"]
SAD_EMOJI_CHOICE = [";-;", ";--;", ";---;", ";___;", ";_;", ";^;", ":(", "(;__;)", "(._.)"]
HAPPY_EMOJI_CHOICE = ["! ", ". ", ". ^ ^ ", " :D ", "! :) ", "! :D ", ":3 ", "<3 ", "\o/ "]
RECOMMAND_CHOICE = ["What kind of restaurant would you like me to recommend?","What kind of restaurant do you like?", "You can tell me type of restaurant you like!"]

EXAMPLE_SENTENCE = ["I want to eat Dimsum for my dinner.", "I want American in medium price.", "Can you give me Cafe restaurant?", "I'm craving Italian for lunch today.", "Where can I find a Grill restaurant?", "I'd like some Sushi for dinner.", "What's a good Bakery for breakfast?", "I'm in the mood for ThaiNortheastern in the evening.", "Is there a Burger place nearby?", "I want to try Healthy cuisine.", "Where can I find a Fusion restaurant in the morning?", "I'm looking for a Halal restaurant.", "I'd like some Icecream for my dessert.", "Is there a Japanese restaurant in town?", "I'm craving Korean for lunch today.", "What's a good Alacarte place?", "I want to eat Streetfood for dinner.", "I'd like some Sukiyaki in low price.", "Can you recommend a Buffet restaurant?", "I'm in the mood for Cafe in the morning.", "I want to try Noodles for dinner.", "Is there a Porkbelly restaurant nearby?", "I'd like some Seafood for my lunch.", "Where can I find a Shabu restaurant?", "I'm craving Breakfast in the evening.", "I want to eat MuKratha for dinner.", "Is there a Ramen restaurant in town?", "I'm looking for a Salad place.", "I'd like some Steak in medium price.", "Can you give me Thai restaurant?", "I'm in the mood for Tea in the morning.", "I want to try American for lunch.", "Is there a Fastfood restaurant nearby?", "I'm craving Dimsum in low price.", "Where can I find a Sushi restaurant?", "I'd like some Bakery for dinner.", "I want to eat ThaiNortheastern in the evening.", "I'm looking for a Grill restaurant.", "Is there a Fusion restaurant in town.", "I'd like some Burger for my dessert.", "I'm in the mood for Healthy cuisine.", "I want to eat Buffet in low price.", "Can you recommend a Cafe restaurant?", "I'm craving Icecream for lunch today.", "Where can I find a Japanese restaurant?", "I'd like some Korean for dinner.", "Is there a Alacarte restaurant nearby.", "I'd like some Seafood for my lunch.", "I'm looking for a Streetfood place.", "I'm in the mood for Sukiyaki in medium price.", "I want to try Sukiyaki for dinner.", "Is there a Tea restaurant in the morning.", "I'd like some Dimsum for dinner.", "Can you give me Fusion restaurant?", "I'm craving Thai for lunch today.", "Where can I find a Shabu restaurant?", "I want to eat Bakery in the evening.", "I'm looking for Ramen in low price.", "I'd like some Grill for dessert.", "Is there a Porkbelly restaurant in town.", "I'm in the mood for MuKratha for my lunch.", "I want to try Salad for dinner.", "Can you recommend a Cafe restaurant?", "I'm craving Breakfast for breakfast.", "Where can I find a Burger restaurant?", "I'd like some Italian in medium price.", "Is there a Halal restaurant nearby.", "I'd like some Noodles for dinner.", "I'm looking for a Seafood place.", "I'm in the mood for Healthy cuisine in the evening.", "I want to eat Icecream in low price.", "Is there a Buffet restaurant in town.", "I'd like some Sushi for lunch today.", "Can you give me American restaurant?", "I'm craving Sukiyaki for dinner.", "Where can I find a Dimsum restaurant?", "I'd like some Tea for dessert.", "I'm in the mood for Fastfood for my lunch.", "I want to try Ramen in the morning.", "Is there a ThaiNortheastern restaurant nearby.", "I'd like some Cafe for dinner.", "I'm looking for Bakery in low price.", "I'm craving Grill for lunch today.", "Where can I find a Steak restaurant?", "I want to eat MuKratha for dinner.", "I'm in the mood for Salad in the evening.", "Is there a Streetfood place in town.", "I'd like some Noodles in medium price.", "Can you recommend a Shabu restaurant?", "I'm craving Seafood for breakfast.", "Where can I find a Korean restaurant?", "I'd like some Japanese for dinner.", "Is there a Alacarte restaurant nearby.", "I'm in the mood for Breakfast for lunch.", "I want to eat Fusion in low price.", "I'd like some Porkbelly for dessert.", "Can you give me Italian restaurant?", "I'm looking for Dimsum for my lunch.", "I'm in the mood for Icecream for dinner.", "Is there a Buffet restaurant in town."]

UNNECESSARY_WORDS = ['!', ',', '.', 'a', '?', 'above', 'after', 'along', 'although', 'among', 'an', 'and', 'anorexic', 'appetite', 'around', 'as', 'at', 'be', 'because', 'before', 'behind', 'below', 'beside', 'besides', 'best', 'between', 'beyond', 'bulimic', 'but', 'by', 'can', 'craving', 'dat', 'deprived', 'dessert', 'do', 'during', 'eat', 'either', 'emaciated', 'every', 'except', 'famished', 'fasting', 'few', 'food', 'food-deprived', 'for', 'from', 'gaunt', 'give', 'good', 'hatyai', 'have', 'hence', 'henceforth', 'her', 'his', 'how', 'hungry', 'i', "i'm", 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'like', 'looking', 'malnourished', 'many', 'me', 'mine', 'more', 'most', 'my', 'near', 'nearby', 'neither', 'no', 'none', 'not', 'of', 'on', 'or', 'our', 'over', 'parched', 'pining', 'please', 'price', 'prices', 'ravenous', 'recommend', 'restaurant', 'restaurants', 'satiated', 'shopsshop', 'since', 'so', 'some', 'songkhla', 'starving', 'store', 'stores', 'such', 'thad', 'thai', 'thailand', 'that', 'the', 'their', 'them', 'there', 'therefore', 'this', 'though', 'through', 'thus', 'to', 'town', 'type', 'u', 'under', 'underfed', 'undernourished', 'unless', 'until', 'us', 'voracious', 'want', 'we', 'what', "what's", 'when', 'where', 'whereas', 'which', 'while', 'who', 'why', 'with', 'within', 'without', 'you', 'your', 'town', 'find']
STOP_WORDS = ['!', ',', '.', '?']