import os
import re
import requests
import time
import random
import datetime

import pandas as pd
import numpy as np

from lxml import html

from .dataset import GREETING_CORPUS, TYPE_CORPUS, PRICE_CHOICES, ANYPRICE_CORPUS, LOW_PRICE_CORPUS, MEDIUM_PRICE_CORPUS, HIGH_PRICE_CORPUS, PRICE_CORPUS, ANYTIME_CORPUS, SPECIFIC_TIME_CORPUS, TIME_CORPUS, RESET_CORPUS, ALL_CORPUS, GREETING_CHOICE, ACCEPTED_CHOICE, SAD_EMOJI_CHOICE, HAPPY_EMOJI_CHOICE, RECOMMAND_CHOICE, LABEL_COLORS, UNNECESSARY_WORDS
from .dataset import df

from . import query_df

from .sentence_model import calculate_similarity_score


def generate_html_list(list):
    result = '<ol class="ui suffixed list">'
    for element in list:
        result += f"<li>{element}</li>"
    return result + "</ol>"


def generate_grey_text(text):
    return f'<span class="ui grey text">{text}</span>'


def check_input_reset(chat, input):
    predict, score = calculate_similarity_score(input, RESET_CORPUS)
    print(
        f'current_state({chat.current_state}) | input: "{input}" | predict: "{predict}" | score: {score}'
    )
    answer = None
    if predict:
        answer = (
            random.choice(ACCEPTED_CHOICE) + " "
            + random.choice(HAPPY_EMOJI_CHOICE)
            + random.choice(RECOMMAND_CHOICE)
        )
   
    return answer

def answer_recommandation(chat):
    result_df = pd.DataFrame([])
    df = dataset.df.copy()
    preferred_types = chat.user.preferred_types
    preferred_prices = chat.user.preferred_prices
    chat.current_state = "none"

    
    if not preferred_types:
        answer = random.choice(GREETING_CHOICE) + random.choice(HAPPY_EMOJI_CHOICE) + "Please select preferred type of restaurants"
        chat.create_bot_message("text", answer)
        return answer
    for type in preferred_types:
        df = query_df.query_type(df, type)
        result_df = pd.concat([result_df, df])
    

    if not preferred_prices:
        answer = random.choice(GREETING_CHOICE) + random.choice(HAPPY_EMOJI_CHOICE) + "Please select preferred price of restaurants"
        chat.create_bot_message("text", answer)
        return answer
    for price_symbol in preferred_prices:
        df = query_df.query_price(df, price_symbol)
        result_df = pd.concat([result_df, df])

    if result_df.empty:
        answer = f"Sorry we cannot find restaurant suite with your prefer {random.choice(SAD_EMOJI_CHOICE)}"
        chat.create_bot_message("text", answer)
        return False
    
    result_df = query_df.query_in_period_time(result_df, datetime.datetime.now().time())
    if result_df.empty:
        answer = f"Not any restaurant are open right now. {random.choice(SAD_EMOJI_CHOICE)}"
        chat.create_bot_message("text", answer)
        return False
        
    answer = f"Here is a list of restaurants we think are right for you. {random.choice(HAPPY_EMOJI_CHOICE)}"
    chat.create_bot_message("text", answer)
    chat.create_bot_message_dataframe(result_df)
    return True


def chat_answer(chat, input):
    reset_answer =  check_input_reset(chat, input)
    if reset_answer:
        chat.create_bot_message("text", reset_answer)
        chat.clear_current_data()
        return 
        
    if "recommand restaurant for me" in input.lower():
        return answer_recommandation(chat)

    input = input.replace(",", "")
    lst_input = input.lower().split()
    for word in lst_input:
        if word in UNNECESSARY_WORDS:
            # This is unnecnessary word something like eg. "what is restaurant", "how", "i want"
            # We keep only important word eg. FastFood, High Price, Midnight
            continue

        predict, score= calculate_similarity_score(word, ALL_CORPUS)
        print(f"\nword: {word} \t=> {predict} \t score: {score}")
        if predict in TYPE_CORPUS:
            print(">catch (type) ", predict)
            chat.current_type = predict
            answer = answer_type(chat, predict)

        elif predict in TIME_CORPUS:
            print(">catch (time) ", predict)
            chat.current_time = predict
            answer = answer_time(chat, predict)

        elif predict in PRICE_CORPUS:
            print(">catch (price) ", predict)
            chat.current_price = predict
            answer = answer_price(chat, predict)

            
    if not chat.current_type and not chat.current_time and not chat.current_type:
        chat.save_current_df(df.copy())
        answer = answer_greeting(chat, input)

    if not chat.current_type:
        answer = answer_type(chat, input)
        if not answer:
            return question_type(chat, input)
        
    if not chat.current_price:
        answer = answer_price(chat, input)
        if not answer:
            return question_price(chat, input)

    if not chat.current_time:
        answer = answer_time(chat, input)
        if not answer:
            return question_time(chat, input)

    if chat.current_time in SPECIFIC_TIME_CORPUS and not chat.selected_time:
        answer = answer_choose_period(chat, input)
        if not answer:
            return question_choose_period(chat, input)
    
    return chat_final_answer_dataframe(chat, chat.current_type, chat.current_price, chat.selected_time)


def answer_greeting(chat, input):
    current_df = chat.get_current_df()

    predict, score = calculate_similarity_score(input, GREETING_CORPUS)
    print(
        f'current_state({chat.current_state}) | input: "{input}" | predict: "{predict}" | score: {score}'
    )
    if predict in GREETING_CORPUS:
        answer = (
            random.choice(GREETING_CHOICE)
            + random.choice(HAPPY_EMOJI_CHOICE)
            + random.choice(RECOMMAND_CHOICE)
            + question_type(chat, input)
        )
    else:
        answer = (
            random.choice(GREETING_CHOICE)
            + random.choice(HAPPY_EMOJI_CHOICE)
            + " Is there anything I can help you with?"
        )
    chat.current_state = "type"
    chat.save()
    chat.save_current_df(current_df)
    return answer

# TYPE
def question_type(chat, input):
    question = "You can tell me type of restaurant you like!" + random.choice(HAPPY_EMOJI_CHOICE)
    if chat.current_state == "type":
        question = f"Based on my data You can try choosing a type of restaurant from this type.! {random.choice(HAPPY_EMOJI_CHOICE)} <p/> <br> {', '.join(TYPE_CORPUS)}"

    chat.create_bot_message("text", question)
    chat.current_state = "type"
    chat.save()

def answer_type(chat, input):
    predict, score = calculate_similarity_score(input.lower(), TYPE_CORPUS)
    print(f'current_state({chat.current_state}) | input: "{input}" | predict: "{predict}" | score: {score}')
    if predict in TYPE_CORPUS:
        chat.current_type = predict
        chat.save()
        return True
    return False

# PRICE
def question_price(chat, input):
    color = LABEL_COLORS[TYPE_CORPUS.index(chat.current_type) % len(LABEL_COLORS)]
    question = f"<div class='ui {color} label'>{chat.current_type}</div> What price range do you prefer? <ol class='ui suffixed list'><li>Low <span class='ui grey text'>(Less than 100 baht)</span></li><li>Medium <span class='ui grey text'>(100 baht - 250 baht)</span></li><li>High <span class='ui grey text'>(More than 250 baht)</span></li><li>Not specific</li></ol> "
    if chat.current_state == "price":
        question = f"Sorry <b>{random.choice(SAD_EMOJI_CHOICE)}</b> We were unable to find an answer for the message {input} with the data. You can try searching with our price information. <p/> <ol class='ui suffixed list'><li>Low <span class='ui grey text'>(Less than 100 Baht)</span></li><li>Medium <span class='ui grey text'>(100 Baht - 250 Baht)</span></li><li>High <span class='ui grey text'>(More than 250 Baht)</span></li><li>Not specific</li></ol>"

    chat.create_bot_message("text", question)
    chat.current_state = "price"
    chat.save()
    return question

def answer_price(chat, input):
    if input == "1":
        input = "low"
    if input == "2":
        input = "medium"
    if input == "3":
        input = "high"
    if input == "4":
        input = "not specific"
    
    predict, score = calculate_similarity_score(input.lower(), PRICE_CORPUS)
    print(f'current_state({chat.current_state}) | input: "{input}" | predict: "{predict}" | score: {score}')
    if predict in PRICE_CORPUS:
        chat.current_price = predict
        if predict in ANYPRICE_CORPUS:
            chat.current_state = "completed"
            chat.save()
            return True
    return False

# TIME
def question_time(chat, input):
    color = ["green", "primary", "red"][PRICE_CORPUS.index(chat.current_price) % 3]
    question = f"<div class='ui {color} label'>{chat.current_price.title()}</div> What time do you want to go? <ol class='ui suffixed list'><li>Anytime</li><li>Choose time</li></ol>"
    if chat.current_state == "time":
        question = f"<div class='ui teal label'>Choose time</div> Try to choose time you want to go again {random.choice(SAD_EMOJI_CHOICE)} <ol class='ui suffixed list'><li>Anytime</li><li>Choose time</li></ol>"

    chat.create_bot_message("text", question)
    chat.current_state = "time"
    chat.save()
    return question

def answer_time(chat, input):
    if input == "1":
        input = "anytime"
    if input == "2":
        input = "choose"
    predict, score = calculate_similarity_score(input.lower(), TIME_CORPUS)
    print(f'current_state({chat.current_state}) | input: "{input}" | predict: "{predict}" | score: {score}')

    if predict in ANYTIME_CORPUS:
        answer = f"Here is a list of restaurants we think are right for you. {random.choice(HAPPY_EMOJI_CHOICE)}"
        chat.create_bot_message("text", answer)
        chat.current_state = "completed"
        chat.current_time = predict
        chat.save()
        return True
    return False

# CHOOSE PERIOD
def question_choose_period(chat, input):
    question = f"<div class='ui teal label'>Choose time</div> Please specify the time you want to go. <span class='ui grey text'>(For example 18:30, 9.15, 10.00)</span>"
    if chat.current_state == "choose_period":
        question = f"<div class='ui purple label'>{input}</div> Please specify the time according to the specified format. <span class='ui grey text'>(For example 18:30, 9.15, 10.00)</span>"

    chat.create_bot_message("text", question)
    chat.current_state = "choose_period"
    chat.save()
    return question

def answer_choose_period(chat, input):
    try:
        select_time = datetime.datetime.strptime(input, "%H.%M").time()
    except:
        try:
            select_time = datetime.datetime.strptime(input, "%H:%M").time()
        except:
            chat.current_state = "choose_period"
            chat.save()
            return False

    chat.selected_time = select_time
    chat.current_state = "completed"
    chat.save()
    return True

# FINAL DATAFRAME
def chat_final_answer_dataframe(chat, type, price, selected_time=None):
    answer = f'Your summary information is: <div class="ui green label">{type.title()}</div> <div class="ui primary label">{price.title()}</div> <div class="ui purple label">{chat.current_time.title()}</div>'
    answer += f'<div class="ui purple label">{selected_time}</div>' if selected_time else ''
    chat.create_bot_message("text", answer)

    unqueried_df = dataset.df.copy()
    df = query_df.query_type(unqueried_df, type)

    if price not in ANYPRICE_CORPUS:
        df = query_df.query_price(df, price)
        if df.empty:
            answer = f"Sorry <b>{random.choice(SAD_EMOJI_CHOICE)}</b> for the information right now. We couldn't find any restaurants in the category you selected for the price ({price}) <br>Here are some restaurants in our ({type}) type that we recommend. We hope you like them. {random.choice(HAPPY_EMOJI_CHOICE)}"
            chat.create_bot_message("text", answer)
            queried_type_df = query_df.query_type(unqueried_df, type)
            chat.create_bot_message_dataframe(queried_type_df)
            return True
    
    if selected_time:
        df = query_df.query_in_period_time(df, selected_time)
        if df.empty:
            selected_time = selected_time.strftime("%H:%M")
            answer = f"Sorry <b>{random.choice(HAPPY_EMOJI_CHOICE)}</b> We couldn't find any restaurants open during the time you selected. ({selected_time}) <br>Here are our recommended restaurants. Hope you like it. {random.choice(HAPPY_EMOJI_CHOICE)}"
            chat.create_bot_message("text", answer)
            queried_price_df = query_df.query_price(df, price)
            chat.create_bot_message_dataframe(queried_price_df)
            return True
    
    answer = f"Here is a list of restaurants we think are right for you. {random.choice(HAPPY_EMOJI_CHOICE)}"
    chat.create_bot_message("text", answer)
    chat.create_bot_message_dataframe(df)
    return True
