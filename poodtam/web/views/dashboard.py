from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from chatbot import chat_answer
from poodtam import models
from chatbot import TYPE_CORPUS

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
    chat = models.Chat.objects(user=user).first()
    if not chat:
        chat = models.Chat()
        chat.user = user
        chat.create_bot_message("text", "Ask me...")
    chat.save()
    return render_template(
        "/dashboard/index.html",
        RESTAURANT_TYPE=TYPE_CORPUS,
        chat=chat,
        is_openning=is_openning,
    )

@module.route("/submit_message", methods=["GET"])
def submit_message():
    user = current_user._get_current_object()
    chat = models.Chat.objects(user=user).first()
    input = request.args.get("input", None)
    if input:
        chat.create_user_message("text", input)
        chat_answer(chat, input)
    chat.save()
    return redirect(url_for('dashboard.index'))