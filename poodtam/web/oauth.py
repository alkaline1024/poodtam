from flask import g, config, session, redirect, url_for, current_app
from flask_login import current_user, login_user
from flask_bcrypt import Bcrypt
from authlib.integrations.flask_client import OAuth

from poodtam import models
import mongoengine as me

import datetime


oauth = OAuth()
bcrypt = Bcrypt()


def fetch_token(name):
    token = models.OAuth2Token.objects(
        name=name, user=current_user._get_current_object()
    ).first()
    return token.to_dict()


def update_token(name, token):
    item = models.OAuth2Token(
        name=name, user=current_user._get_current_object()
    ).first()
    item.token_type = token.get("token_type", "Bearer")
    item.access_token = token.get("access_token")
    item.refresh_token = token.get("refresh_token")
    item.expires = datetime.datetime.utcfromtimestamp(token.get("expires_at"))

    item.save()
    return item


def create_user(form):
    username = form.username.data
    password = bcrypt.generate_password_hash(form.password.data)
    user = models.User.objects(username=username).first()
    if not user:
        user = models.User(
            name=form.name.data,
            username=username,
            password=password,
            email=form.email.data,
            is_active=True,
            last_login_date=datetime.datetime.now(),
        )
        user.save()
        login_user(user)
        return True
    return False


def handle_authorized_user(form):
    username = form.username.data
    password = form.password.data
    user = models.User.objects(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        user.save()
        return True
    return False


def init_oauth(app):
    oauth.init_app(app, fetch_token=fetch_token, update_token=update_token)


def init_bcrypt(app):
    bcrypt.init_app(app)