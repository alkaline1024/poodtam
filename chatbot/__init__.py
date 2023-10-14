import datetime
import re
import requests
import random
from lxml import html
import pandas as pd

# module selenium
import time
import numpy as np
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from sentence_transformers import SentenceTransformer, util

import os

model = SentenceTransformer(
    "sentence-transformers/distiluse-base-multilingual-cased-v2"
)
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

df_types = df["type"].str.split(", ").tolist()
TYPE_CORPUS = list(set([word for sublist in df_types for word in sublist]))


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
UNNECESSARY_WORDS = [
    "give",
    "me",
    "please",
    "i",
    "want",
    "restaurant",
    "store",
    "some",
    "can",
    "you",
    "type",
]


RESET_CORPUS = [
    "reset",
    "restart",
    "again",
]

ALL_CORPUS = GREETING_CORPUS + TYPE_CORPUS + PRICE_RANGE_CORPUS + TIME_CORPUS

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


def generate_html_list(list):
    result = '<ol class="ui suffixed list">'
    for element in list:
        result += f"<li>{element}</li>"
    return result + "</ol>"


def generate_grey_text(text):
    return f'<span class="ui grey text">{text}</span>'

def calculate_similarity_score(question, corpus):
    lst_question = question.lower().split()
    for word in UNNECESSARY_WORDS:
        if word in lst_question:
            lst_question.remove(word)

    cleaned_question = "".join(lst_question)

    question_vec = model.encode(
        cleaned_question, convert_to_tensor=True, normalize_embeddings=True
    )
    corpus_vec = model.encode(corpus, convert_to_tensor=True, normalize_embeddings=True)

    cosine_scores = util.cos_sim(question_vec, corpus_vec)
    entity_vector = np.array(cosine_scores)

    score = np.max(entity_vector)
    if score >= 0.6:
        match_entity = corpus[np.argmax(entity_vector)]
        return match_entity, score
    return None, score


current_df = df.copy()
current_state = None

def chat_answer(input):
    global current_df
    global current_state

    answer = None
    status = None

    answer, status =  check_input_reset(input)
    if answer:
        return answer, status, current_df


    if current_state == None:
        current_df = df.copy()
        answer, status = get_answer_state_greeting(input)

    elif "type" in current_state:
        current_df = df.copy()
        answer, status = get_answer_state_type(input)

    elif "price" in current_state:
        answer, status = get_answer_state_price(input)

    elif "time" in current_state:
        answer, status = get_answer_state_time(input)

    elif "choose_period" in current_state:
        answer, status = get_answer_choose_period(input)

    print(current_df)

    return answer, status, current_df

def check_input_reset(input):
    predict, score = calculate_similarity_score(input, RESET_CORPUS)
    print(
        f'state({current_state}) | input: "{input}" | predict: "{predict}" | score: {score}'
    )
    answer = None
    status = None
    if predict:
        status = "process"
        answer = (
            random.choice(ACCEPTED_CHOICE) + " "
            + random.choice(HAPPY_EMOJI_CHOICE)
            + random.choice(RECOMMAND_CHOICE)
        )
   
    return answer, status

def get_answer_state_greeting(input):
    global current_df
    global current_state

    status = None
    predict, score = calculate_similarity_score(input, GREETING_CORPUS)
    print(
        f'state({current_state}) | input: "{input}" | predict: "{predict}" | score: {score}'
    )
    if predict in GREETING_CORPUS:
        current_state = "type"
        answer = (
            random.choice(GREETING_CHOICE)
            + random.choice(HAPPY_EMOJI_CHOICE)
            + random.choice(RECOMMAND_CHOICE)
        )
        status = "process"
    else:
        current_state = "type"
        answer = (
            random.choice(GREETING_CHOICE)
            + random.choice(HAPPY_EMOJI_CHOICE)
            + " Is there anything I can help you with?"
        )
        status = "process"

    return answer, status


def get_answer_state_type(input):
    global current_df
    global current_state

    status = None
    predict, score = calculate_similarity_score(input.lower(), TYPE_CORPUS)
    print(
        f'state({current_state}) | input: "{input}" | predict: "{predict}" | score: {score}'
    )
    if predict in TYPE_CORPUS:
        current_state = "price"
        color = LABEL_COLORS[TYPE_CORPUS.index(predict) % len(LABEL_COLORS)]
        answer = f"<div class='ui {color} label'>{predict}</div> What price range do you prefer? <ol class='ui suffixed list'><li>Low <span class='ui grey text'>(Less than 100 baht)</span></li><li>Medium <span class='ui grey text'>(100 baht - 250 baht)</span></li><li>High <span class='ui grey text'>(More than 250 baht)</span></li><li>Not specific</li></ol> "
        current_df = current_df[current_df["type"].str.contains(predict)]
        status = "process"
    elif current_state == "type":
        current_state = "type2"
        answer = "You can tell me type of restaurant you like!" + random.choice(HAPPY_EMOJI_CHOICE)
        status = "process"
    else:
        current_state = "type3"
        answer = f"Based on my data You can try choosing a type of restaurant from this type.! {random.choice(HAPPY_EMOJI_CHOICE)} <p/> <br> {', '.join(TYPE_CORPUS)}"
        status = "process"

    return answer, status


def get_answer_state_price(input):
    global current_df
    global current_state

    if input == "1":
        input = "low"
    if input == "2":
        input = "medium"
    if input == "3":
        input = "high"
    if input == "4":
        input = "not specific"

    status = None
    predict, score = calculate_similarity_score(input.lower(), PRICE_RANGE_CORPUS)
    print(
        f'state({current_state}) | input: "{input}" | predict: "{predict}" | score: {score}'
    )
    if predict in PRICE_RANGE_CORPUS:
        current_state = "time"
        status = "process"
        color = ["green", "primary", "red"][PRICE_RANGE_CORPUS.index(predict) % 3]
        answer = f"<div class='ui {color} label'>{predict}</div> What time do you want to go? <ol class='ui suffixed list'><li>Anytime</li><li>Choose time</li></ol>"
        if predict in ANYPRICE_CORPUS:
            return answer, status
        if predict in LOW_PRICE_CORPUS:
            price_symbol = "฿"
        elif predict in MEDIUM_PRICE_CORPUS:
            price_symbol = "฿฿"
        elif predict in HIGH_PRICE_CORPUS:
            price_symbol = "฿฿฿"
        current_df = current_df[current_df["price"] == price_symbol]
        if current_df.empty:
            status = "completed"
            current_state = None
            current_df = df[df["price"] == price_symbol]
            answer = f"Sorry <b>{random.choice(SAD_EMOJI_CHOICE)}</b> for the information right now. We couldn't find any restaurants in the category you selected for the price ({input}) <br>Here are some restaurants in our ({input}) price range that we recommend. We hope you like them. {RANDOM_HAPPY_EMOJI}"
    else:
        answer = f"Sorry <b>{random.choice(SAD_EMOJI_CHOICE)}</b> We were unable to find an answer for the message {input} with the data. You can try searching with our price information. <p/> <ol class='ui suffixed list'><li>Low <span class='ui grey text'>(Less than 100 Baht)</span></li><li>Medium <span class='ui grey text'>(100 Baht - 250 Baht)</span></li><li>High <span class='ui grey text'>(More than 250 Baht)</span></li><li>Not specific</li></ol>"
        status = None

    return answer, status


def get_answer_state_time(input):
    global current_df
    global current_state

    if input == "1":
        input = "anytime"
    if input == "2":
        input = "choose"

    try:
        select_time = datetime.datetime.strptime(input, "%H.%M").time()
    except:
        select_time = input
    if isinstance(select_time, datetime.time):
        try:
            select_time = datetime.datetime.strptime(input, "%H:%M").time()
        except:
            select_time = input

    status = None
    predict, score = calculate_similarity_score(input.lower(), TIME_CORPUS)
    print(
        f'state({current_state}) | input: "{input}" | predict: "{predict}" | score: {score}'
    )
    if predict in ANYTIME_CORPUS:
        current_state = None
        answer = f"Here is a list of restaurants we think are right for you. {random.choice(HAPPY_EMOJI_CHOICE)}"
        status = "completed"
    elif predict in SPECIFIC_TIME_CORPUS:
        current_state = "choose_period"
        answer = f"<div class='ui teal label'>Choose time</div> Please specify the time you want to go. <span class='ui grey text'>(For example 18:30, 9.15, 10.00)</span>"
        status = "process"
    else:
        current_state = "time"
        answer = f"<div class='ui teal label'>Choose time</div> Try to choose time you want to go again {random.choice(SAD_EMOJI_CHOICE)} <ol class='ui suffixed list'><li>Anytime</li><li>Choose time</li></ol>"

    return answer, status


def get_answer_choose_period(input):
    global current_df
    global current_state

    try:
        select_time = datetime.datetime.strptime(input, "%H.%M").time()
    except:
        try:
            select_time = datetime.datetime.strptime(input, "%H:%M").time()
        except:
            answer = f"<div class='ui purple label'>{input}</div> Please specify the time according to the specified format. <span class='ui grey text'>(For example 18:30, 9.15, 10.00)</span>"
            status = "error"
            return answer, status

    unquery_df = current_df.copy()
    current_df = current_df[
        (current_df["opening time"] <= select_time)
        & (select_time <= current_df["closing time"])
    ]

    if not current_df.empty:
        answer = f"Here is a list of restaurants we think are right for you. {random.choice(HAPPY_EMOJI_CHOICE)}"
    else:
        answer = f"Sorry <b>{random.choice(HAPPY_EMOJI_CHOICE)}</b> We couldn't find any restaurants open during the time you selected. ({input}) <br>Here are our recommended restaurants. Hope you like it. {RANDOM_HAPPY_EMOJI}"
        current_df = unquery_df.copy()

    status = "completed"
    current_state = None

    return answer, status
