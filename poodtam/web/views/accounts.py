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
    return redirect(url_for("accounts.login", login_status="failed"))


@module.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit():
    user = current_user._get_current_object()
    form = forms.accounts.ProfileForm(obj=user)
    if not form.validate_on_submit():
        return render_template("accounts/edit.html", form=form)

    user = current_user._get_current_object()
    form.populate_obj(user)
    user.save()
    flash("Saved Successfully!")
    return render_template("accounts/edit.html", form=form)