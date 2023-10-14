import mongoengine as me
import datetime
from flask_login import UserMixin


class User(me.Document, UserMixin):
    meta = {"collection": "users", "strict": False}

    username = me.StringField(required=True, unique=True)
    password = me.BinaryField(required=True)

    name = me.StringField(required=True)
    email = me.StringField(required=True)
    description = me.StringField()
    picture = me.ImageField(thumbnail_size=(800, 600, True))

    roles = me.ListField(me.StringField(), default=["user"])

    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    updated_date = me.DateTimeField(required=True, default=datetime.datetime.now)

    is_active = me.BooleanField(required=True)
    last_login_date = me.DateTimeField(
        required=True, default=datetime.datetime.now, auto_now=True
    )