import mongoengine as me
import pandas as pd
import datetime
import json
import io
from bson.objectid import ObjectId

class Message(me.EmbeddedDocument):
    uid = me.ObjectIdField(required=True, default=ObjectId)
    type = me.StringField(required=True, choices=["text", "dataframe"])
    text = me.StringField(required=True)
    sender = me.StringField(choices=["user", "bot"], required=True)

    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)

    def get_dataframe(self):
        if self.type == "dataframe":
            try:
                df = pd.read_json(io.StringIO(self.text))
                df['opening time'] = pd.to_datetime(df['opening time'], format="%H:%M:%S")
                df['closing time'] = pd.to_datetime(df['closing time'], format="%H:%M:%S")
                return df
            except Exception as error:
                return pd.DataFrame([])
        return pd.DataFrame([])

class Chat(me.Document):
    meta = {"collection": "chats"}

    user = me.ReferenceField("User", required=True)
    messages = me.EmbeddedDocumentListField(Message)

    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    updated_date = me.DateTimeField(required=True, default=datetime.datetime.now)

    def create_bot_message(self, type:str, text:str):
        message = Message(type=type, text=text, sender="bot")
        self.messages.append(message)

    def create_user_message(self, type:str, text:str):
        message = Message(type=type, text=text, sender="user")
        self.messages.append(message)

