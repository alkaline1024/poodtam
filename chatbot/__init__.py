import os
import re
import requests
import time
import random
import datetime
import copy

import pandas as pd
import numpy as np

from lxml import html

from .dataset import GREETING_CORPUS, TYPE_CORPUS, PRICE_CHOICES, ANYPRICE_CORPUS, LOW_PRICE_CORPUS, MEDIUM_PRICE_CORPUS, HIGH_PRICE_CORPUS, PRICE_CORPUS, ANYTIME_CORPUS, SPECIFIC_TIME_CORPUS, TIME_CORPUS, RESET_CORPUS, ALL_CORPUS, GREETING_CHOICE, ACCEPTED_CHOICE, SAD_EMOJI_CHOICE, HAPPY_EMOJI_CHOICE, RECOMMAND_CHOICE, LABEL_COLORS, UNNECESSARY_WORDS, TYPE_CHOICES_HTML, CHOOSE_TIME_CORPUS, NOW_TIME_CORPUS, BREAKFAST_CORPUS, LUNCH_CORPUS, DINNER_CORPUS, STOP_WORDS
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
    df = dataset.df.copy()
    preferred_types = chat.user.preferred_types
    preferred_prices = chat.user.preferred_prices
    user_preferred_type_html = ' '.join([f'<div class="ui teal label">{type}</div>' for type in chat.user.preferred_types])
    user_preferred_price_html = ' '.join([f'<div class="ui teal label">{price}</div>' for price in chat.user.preferred_prices])
    
    chat.current_state = "none"
    
    answer = ""
    if not preferred_types:
        answer += '<p>' + random.choice(GREETING_CHOICE) + random.choice(HAPPY_EMOJI_CHOICE) + "You didn't select preferred type of restaurants, You can setting in <a href='/edit-profile'>Edit Profile</a></p>"
    if not preferred_prices:
        answer += '<p>' + random.choice(GREETING_CHOICE) + random.choice(HAPPY_EMOJI_CHOICE) + "You didn't select preferred price of restaurants, You can setting in <a href='/edit-profile'>Edit Profile</a></p>"
    if answer:
        chat.create_bot_message("text", answer)

    if not preferred_types and not preferred_prices:
        answer = f"{random.choice(HAPPY_EMOJI_CHOICE)} {random.choice(HAPPY_EMOJI_CHOICE)} But don't worry We have some restaurant recommand to you !"
        random_df = dataset.df.sample(n=5, replace=False)
        chat.create_bot_message("text", answer)
        chat.create_bot_message_dataframe(random_df)
        return True
    
    type_df = pd.DataFrame([])
    for type in preferred_types:
        type_df = pd.concat([type_df, query_df.query_type(df, type)], ignore_index=True)
    
    price_df = pd.DataFrame([])
    for price_symbol in preferred_prices:
        if type_df.empty:
            price_df = pd.concat([price_df, query_df.query_price(df, price_symbol)], ignore_index=True)
        else:
            price_df = pd.concat([price_df, query_df.query_price(type_df, price_symbol)], ignore_index=True)

    selected_df = type_df if not preferred_prices else price_df
    if selected_df.empty:
        answer = f"This is restaurant base on your setting prefers. If you don't like {random.choice(SAD_EMOJI_CHOICE)} you can change at <a href='/edit-profile'>Edit Profile</a></p> {random.choice(HAPPY_EMOJI_CHOICE)} <p><div class='ui brown horizontal label'>Types</div> {user_preferred_type_html}</p><p><div class='ui green horizontal label'>Prices</div> {user_preferred_price_html}</p></p>"
        chat.create_bot_message("text", answer)
        chat.create_bot_message_dataframe(type_df)
        return False
    
    final_df = query_df.query_in_period_now(selected_df)
    if final_df.empty:
        answer = f"Not any restaurant are open right now. {random.choice(SAD_EMOJI_CHOICE)}"
        chat.create_bot_message("text", answer)
        return False
        
    answer = f"Here is a list of restaurants you must liked it. {random.choice(HAPPY_EMOJI_CHOICE)}"
    chat.create_bot_message("text", answer)
    chat.create_bot_message_dataframe(final_df)

    answer = f"{random.choice(GREETING_CHOICE)} {random.choice(HAPPY_EMOJI_CHOICE)} I just give you recommandation about restaurant {random.choice(HAPPY_EMOJI_CHOICE)} <p></p> This data is based on your prefers. If you don't like {random.choice(SAD_EMOJI_CHOICE)} you can change at <a href='/edit-profile'>Edit Profile</a><p><div class='ui brown horizontal label'>Types</div> {user_preferred_type_html}</p><p><div class='ui green horizontal label'>Prices</div> {user_preferred_price_html}</p>"
    chat.create_bot_message("text", answer)
    answer = f"We hope you liked it. {random.choice(HAPPY_EMOJI_CHOICE)}"
    chat.create_bot_message("text", answer)
    return True


def chat_answer(chat, input):
    reset_answer =  check_input_reset(chat, input)
    if reset_answer:
        chat.create_bot_message("text", reset_answer)
        chat.clear_current_data()
        return 
        
    if "recommand restaurant for me" in input.lower():
        return answer_recommandation(chat)

    copy_input = copy.copy(input)
    # CLEAR STOP WORDS
    for stopword in STOP_WORDS:
        input = input.replace(stopword, "")

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

    if chat.current_time.lower() in SPECIFIC_TIME_CORPUS:
        answer = answer_specific_time(chat, copy_input)
        if not answer:
            return question_specific_time(chat, input)
    
    return chat_final_answer_dataframe(chat)


def answer_greeting(chat, input):
    current_df = chat.get_current_df()

    predict, score = calculate_similarity_score(input, GREETING_CORPUS)
    print(
        f'current_state({chat.current_state}) | input: "{input}" | predict: "{predict}" | score: {score}'
    )
    if predict in GREETING_CORPUS:
        question_type(chat, input)
    else:
        answer = (
            random.choice(GREETING_CHOICE)
            + random.choice(HAPPY_EMOJI_CHOICE)
            + " Is there anything I can help you with?"
        )
    chat.current_state = "type"
    chat.save()
    chat.save_current_df(current_df)
    return True

# TYPE
def question_type(chat, input):

    question = f"{random.choice(GREETING_CHOICE)} {random.choice(HAPPY_EMOJI_CHOICE)} {random.choice(RECOMMAND_CHOICE)} {random.choice(HAPPY_EMOJI_CHOICE)}"
    if chat.current_state == "type":
        question = f"Based on my data You can try choosing a type of restaurant from this type.! {random.choice(HAPPY_EMOJI_CHOICE)} <p/> <br> {TYPE_CHOICES_HTML}"

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
    question = f"<div class='ui {color} label'>{chat.current_type}</div> What price range do you prefer? <ol class='ui suffixed list'><li>Low <span class='ui grey text'>(Less than 100 baht)</span></li><li>Medium <span class='ui grey text'>(100 baht - 250 baht)</span></li><li>High <span class='ui grey text'>(More than 250 baht)</span></li><li>Anyprice</li></ol> "
    if chat.current_state == "price":
        question = f"Sorry <b>{random.choice(SAD_EMOJI_CHOICE)}</b> We were unable to find an answer for the message {input} with the data. You can try searching with our price information. <p/> <ol class='ui suffixed list'><li>Low <span class='ui grey text'>(Less than 100 Baht)</span></li><li>Medium <span class='ui grey text'>(100 Baht - 250 Baht)</span></li><li>High <span class='ui grey text'>(More than 250 Baht)</span></li><li>Any Price</li></ol>"

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
        input = "anyprice"
    
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
    color = ["brown", "green", "red"][PRICE_CORPUS.index(chat.current_price) % 3]
    question = f"<div class='ui {color} label'>{chat.current_price.title()}</div> What time do you want to go? <ol class='ui suffixed list'><li>Now</li><li>Breakfast</li><li>Lunch</li><li>Dinner</li><li>Specific time</li><li>Anytime</li></ol>"
    if chat.current_state == "time":
        question = f"<div class='ui teal label'>Choose time</div> Try to choose time you want to go again {random.choice(SAD_EMOJI_CHOICE)} <ol class='ui suffixed list'><li>Now</li><li>Breakfast</li><li>Lunch</li><li>Dinner</li><li>Specific time</li><li>Anytime</li></ol>"

    chat.create_bot_message("text", question)
    chat.current_state = "time"
    chat.save()
    return question

def answer_time(chat, input):
    if input == "1":
        input = "Now"
    elif input == "2":
        input = "Breakfast"
    elif input == "3":
        input = "Lunch"
    elif input == "4":
        input = "Dinner"
    elif input == "5":
        input = "Specific"
    elif input == "6":
        input = "Anytime"

    predict, score = calculate_similarity_score(input.lower(), TIME_CORPUS)
    print(f'current_state({chat.current_state}) | input: "{input}" | predict: "{predict}" | score: {score}')

    if predict in ANYTIME_CORPUS:
        answer = f"Here is a list of restaurants you must liked it. {random.choice(HAPPY_EMOJI_CHOICE)}"
        chat.create_bot_message("text", answer)
        chat.current_state = "completed"
        chat.current_time = predict
        chat.save()
        return True
    elif predict in CHOOSE_TIME_CORPUS:
        chat.current_state = "completed"
        chat.current_time = predict
        if predict in NOW_TIME_CORPUS:
            chat.selected_time = datetime.datetime.now()
        elif predict in BREAKFAST_CORPUS:
            chat.selected_time = datetime.datetime.now().replace(hour=8)
        elif predict in LUNCH_CORPUS:
            chat.selected_time = datetime.datetime.now().replace(hour=12)
        elif predict in DINNER_CORPUS:
            chat.selected_time = datetime.datetime.now().replace(hour=16)
        chat.save()
        return True
    elif predict in SPECIFIC_TIME_CORPUS:
        return False
    return False

# CHOOSE PERIOD
def question_specific_time(chat, input):
    chat.current_time = 'specific'
    question = f"<div class='ui teal label'>Choose time</div> Please specify the time you want to go. <span class='ui grey text'>(For example 18:30, 9.15, 10.00)</span>"
    if chat.current_state == "choose_period":
        question = f"<div class='ui purple label'>{input}</div> Please specify the time according to the specified format. <span class='ui grey text'>(For example 18:30, 9.15, 10.00)</span>"

    chat.create_bot_message("text", question)
    chat.current_state = "choose_period"
    chat.save()
    return question

def answer_specific_time(chat, input):
    try:
        select_time = datetime.datetime.strptime(input, "%H.%M")
        chat.selected_time = select_time
    except:
        try:
            select_time = datetime.datetime.strptime(input, "%H:%M")
            chat.selected_time = select_time
        except:
            chat.current_state = "choose_period"
            chat.save()
            return False

    chat.current_state = "completed"
    chat.save()
    return True

# FINAL DATAFRAME
def chat_final_answer_dataframe(chat):
    chat.current_state = "completed"

    unqueried_df = dataset.df.copy()
    df = query_df.query_type(unqueried_df, chat.current_type)

    if chat.current_price not in ANYPRICE_CORPUS:
        df = query_df.query_price(df, chat.current_price)
        if df.empty:
            queried_type_df = query_df.query_type(unqueried_df, chat.current_type)
            answer = f"Sorry <b>{random.choice(SAD_EMOJI_CHOICE)}</b> for the information right now. We couldn't find any <div class='ui brown label'>{chat.current_type}</div> for the <div class='ui green label'>{chat.current_price.title()}</div> price. <p></p>Here are <div class='ui brown label'>{chat.current_type}</div> that we recommend. We hope you like them. {random.choice(HAPPY_EMOJI_CHOICE)}"
            chat.create_current_information()
            chat.create_bot_message_dataframe(queried_type_df)
            chat.create_bot_message("text", answer)
            return True
    
    if chat.selected_time:
        df = query_df.query_in_period_time(df, chat)
        if df.empty:
            selected_time = chat.selected_time.strftime("%H:%M")
            queried_price_df = query_df.query_price(unqueried_df, chat.current_price)
            answer = f"Sorry <b>{random.choice(HAPPY_EMOJI_CHOICE)}</b> We could not find any restaurants open during the time you selected. <div class='ui purple label'>{selected_time}<div class='detail'>{chat.current_time.title()}</div></div> <p/>Here are our recommended restaurants. Hope you like it. {random.choice(HAPPY_EMOJI_CHOICE)}"
            chat.create_current_information()
            chat.create_bot_message_dataframe(queried_price_df)
            chat.create_bot_message("text", answer)
            return True
    
    answer = f"Here is a list of restaurants you must liked it. {random.choice(HAPPY_EMOJI_CHOICE)}"
    chat.create_current_information()
    chat.create_bot_message_dataframe(df)
    chat.create_bot_message("text", answer)
    return True
