import mongoengine as me
import pandas as pd
import datetime
import json
import io
from bson.objectid import ObjectId
from chatbot import dataset

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

    name = me.StringField()
    
    user = me.ReferenceField("User", required=True)
    messages = me.EmbeddedDocumentListField(Message)

    current_df = me.StringField()
    current_state = me.StringField()
    
    # current data for predict user
    current_type = me.StringField()
    current_price = me.StringField()
    current_time = me.StringField()
    selected_time = me.DateTimeField()

    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    updated_date = me.DateTimeField(required=True, default=datetime.datetime.now)

    def create_user_message(self, type:str, text:str):
        message = Message(type=type, text=text, sender="user")
        self.messages.append(message)
        self.save()

    def create_bot_message(self, type:str, text:str):
        message = Message(type=type, text=text, sender="bot")
        self.messages.append(message)
        self.save()

    def create_bot_message_dataframe(self, df):
        message = Message(type="dataframe", text=df.to_json(), sender="bot")
        self.messages.append(message)
        self.save()

    def create_current_information(self):
        answer = f'Your summary information is: <div class="ui brown label">{self.current_type.title()}<div class="detail">Type</div></div> <div class="ui green label">{self.current_price.title()}<div class="detail">Price</div></div> <div class="ui purple label">{self.current_time.title()}<div class="detail">Time</div></div>'
        answer += f'<div class="ui purple label">{self.selected_time.strftime("%H:%M")}<div class="detail">Time</div></div>' if self.selected_time and self.current_time not in dataset.CHOOSE_TIME_CORPUS else ''
        self.create_bot_message("text", answer)

    def save_current_df(self, df):
        if df is not None:
            self.current_df = str(df.to_json())
            self.save()
        
    def get_current_df(self):
        try:
            df = pd.read_json(io.StringIO(self.current_df))
            return df
        except Exception as error:
            print(error)
            
        return pd.DataFrame([])
    
    # type, price, time
    def clear_current_data(self):
        self.current_type = ""
        self.current_time = ""
        self.selected_time = None
        self.current_price = ""
        self.current_state = "none"
        self.save()
    
    