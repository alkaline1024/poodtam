from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from poodtam import models
from chatbot import chat_answer
from chatbot import TYPE_CORPUS as RESTAURANT_TYPE
from chatbot.dataset import EXAMPLE_SENTENCE

import random
import datetime
import time
import pandas as pd
import io

module = Blueprint("dashboard", __name__, url_prefix="/")


def is_openning(opened_time, closed_time):
    now_time = datetime.datetime.now().time()
    if now_time > opened_time.time() and now_time < closed_time.time():
        return True
    return False

@module.route("/", methods=["GET"])
@login_required
def index():
    user = current_user._get_current_object()
    chats = models.Chat.objects(user=user).order_by("-created_date")

    chat_id = request.args.get("chat_id", None)
    chat = models.Chat.objects(user=user).first()
    if chat_id:
        chat = models.Chat.objects.get(id=chat_id)
        
    if not chat:
        chat = models.Chat()
        chat.user = user
        chat.name = f"Chat {models.Chat.objects().count() + 1}"
        chat.create_bot_message("text", "Ask me...")
        chat.save()
    return render_template(
        "/dashboard/index.html",
        chat=chat,
        chats=chats,
        is_openning=is_openning,
        RESTAURANT_TYPE=RESTAURANT_TYPE,
    )

@module.route("/submit_message/<chat_id>", methods=["GET"])
def submit_message(chat_id):
    user = current_user._get_current_object()
    chat = models.Chat.objects.get(id=chat_id)
    input = request.args.get("input", None)
    if input:
        chat.create_user_message("text", input)
        chat_answer(chat, input)
    chat.save()
    return redirect(url_for('dashboard.index', chat_id=chat.id))

@module.route("/random_sentence")
def random_sentence():
    sentence = random.choice(EXAMPLE_SENTENCE)
    return sentence