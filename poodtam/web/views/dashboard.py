from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from chatbot import chat_answer
from poodtam import models

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


result = "Ask me..."
status = "process"
df = None



@module.route("/", methods=["GET", "POST"])
@login_required
def index():
    user = current_user._get_current_object()
    chat = models.Chat.objects(user=user).first()
    if not chat:
        chat = models.Chat()
        chat.create_bot_message("text", "Ask me...")
        chat.user = user

    global result
    global status
    global df

    input = request.form.get("input", None)
    if input:
        chat.create_user_message("text", input)

        result, status, df = chat_answer(input)

        chat.create_bot_message("text", result)
        if status == "completed" and df is not None:
            chat.create_bot_message("dataframe", str(df.to_json()))

    chat.save()

    return render_template(
        "/dashboard/index.html",
        chat=chat,
        input=input,
        result=result,
        status=status,
        df=df,
        df_exist=df is not None,
        is_openning=is_openning,
    )
