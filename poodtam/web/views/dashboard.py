from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from chatbot import chat_answer
import datetime

module = Blueprint("dashboard", __name__, url_prefix="/")


def is_openning(opened_time, closed_time):
    now_time = datetime.datetime.now().time()
    if now_time > opened_time and now_time < closed_time:
        return True
    return False


result = "Ask me..."
status = "process"
df = None



@module.route("/", methods=["GET", "POST"])
@login_required
def index():
    global result
    global status
    global df

    input = request.form.get("input", None)

    if input:
        result, status, df = chat_answer(input)

    return render_template(
        "/dashboard/index.html",
        input=input,
        result=result,
        status=status,
        df=df,
        df_exist=df is not None,
        is_openning=is_openning,
    )
