from flask_mongoengine import MongoEngine

from .chats import Chat
from .users import User
from .oauth import OAuth2Token


db = MongoEngine()


def init_db(app):
    db.init_app(app)
