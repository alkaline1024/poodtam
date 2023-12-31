import datetime
import markdown
import mongoengine as me

from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    request,
    session,
    current_app,
    send_file,
    abort,
    flash,
)
from flask_login import login_user, logout_user, login_required, current_user

from .. import models
from .. import oauth
from .. import acl
from .. import forms

module = Blueprint("accounts", __name__)


@module.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = forms.accounts.LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        user = models.User.objects(username=username).first()
        if user and oauth.handle_authorized_user(form):
            return redirect(url_for("dashboard.index"))
        flash('Incorrect username or password.')
    return render_template("accounts/login.html", form=form)


@module.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()

    return redirect(url_for("dashboard.index"))

@module.route("/register", methods=["GET", "POST"])
def register():
    form = forms.accounts.RegistrationForm()
    if not form.validate_on_submit():
        return render_template("accounts/register.html", form=form)

    if oauth.create_user(form):
        return redirect(url_for("accounts.login"))
    
    flash("Username already exists")
    return render_template("accounts/register.html", form=form)


@module.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit():
    user = current_user._get_current_object()
    chats = models.Chat.objects(user=user).order_by("-created_date")
    chat = chats.first()
    form = forms.accounts.ProfileForm(obj=user)
    if not form.validate_on_submit():
        return render_template("accounts/edit.html", chats=chats, chat=chat, form=form)

    user = current_user._get_current_object()
    form.populate_obj(user)
    if form.pic.data:
        print(form.pic.data)
        if user.picture:
            user.picture.replace(
                form.pic.data,
                filename=form.pic.data.filename,
                content_type=form.pic.data.content_type,
            )
        else:
            user.picture.put(
                form.pic.data,
                filename=form.pic.data.filename,
                content_type=form.pic.data.content_type,
            )


    user.save()
    flash("Saved Successfully!")
    return render_template("accounts/edit.html", chats=chats, chat=chat, form=form)

@module.route("/accounts/<user_id>/picture/<filename>", methods=["GET", "POST"])
def picture(user_id, filename):
    user = models.User.objects.get(id=user_id)

    if not user or not user.picture or user.picture.filename != filename:
        return abort(403)

    response = send_file(
        user.picture,
        download_name=user.picture.filename,
        mimetype=user.picture.content_type,
    )
    return response



@module.route("/new_chat")
@login_required
def new_chat():
    chat = models.Chat()
    chat.user = current_user._get_current_object()
    chat.name = f"Chat {models.Chat.objects().count() + 1}"
    chat.create_bot_message("text", "Ask me...")
    chat.save()

    return redirect(url_for("dashboard.index", chat_id=chat.id))


@module.route("/chats/<chat_id>/delete")
@login_required
def delete_chat(chat_id):
    chat = models.Chat.objects.get(id=chat_id)
    chat.delete()

    return redirect(url_for("dashboard.index"))

