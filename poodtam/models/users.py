import mongoengine as me
import datetime

from flask import url_for
from flask_login import UserMixin

from chatbot import TYPE_CORPUS, PRICE_CHOICES


class User(me.Document, UserMixin):
    meta = {"collection": "users", "strict": False}

    username = me.StringField(required=True, unique=True, max_length=255)
    password = me.BinaryField(required=True)

    name = me.StringField(required=True, max_length=255)
    email = me.StringField(required=True)
    description = me.StringField()
    picture = me.ImageField(thumbnail_size=(800, 600, True))

    roles = me.ListField(me.StringField(), default=["user"])

    # bot prediction
    preferred_types = me.ListField(me.StringField(), choices=TYPE_CORPUS)
    preferred_prices = me.ListField(me.StringField(), choices=PRICE_CHOICES)

    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    updated_date = me.DateTimeField(required=True, default=datetime.datetime.now)

    is_active = me.BooleanField(required=True)
    last_login_date = me.DateTimeField(
        required=True, default=datetime.datetime.now, auto_now=True
    )

    def get_picture(self):
        if self.picture:
            return url_for(
                "accounts.picture", user_id=self.id, filename=self.picture.filename
            )
        return False
