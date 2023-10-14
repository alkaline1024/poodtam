from wtforms import validators
from wtforms import fields

from flask_wtf import FlaskForm
from flask_mongoengine.wtf import model_form

from poodtam import models

from chatbot import TYPE_CORPUS

BaseRegistrationForm = model_form(
    models.User,
    FlaskForm,
    exclude=[
        "email",
        "picture",
        "roles",
        "created_date",
        "updated_date",
        "is_active",
        "last_login_date",
    ],
    field_args={
        "username": {"label": "Username"},
        "name": {"label": "Display Name"},
    },
)


class RegistrationForm(BaseRegistrationForm):
    password = fields.PasswordField(
        "Password",
        validators=[validators.DataRequired(), validators.EqualTo("password")],
    )
    confirm_password = fields.PasswordField(
        "Confirm Password",
        validators=[validators.DataRequired(), validators.EqualTo("password")],
    )
    email = fields.StringField(
        "Email", validators=[validators.Email(), validators.Optional()]
    )
    favorite_types = fields.SelectMultipleField("Favorite Types of Restaurants", choices=TYPE_CORPUS)


# Define the user login form
class LoginForm(FlaskForm):
    username = fields.StringField(
        "Username", validators=[validators.DataRequired()]
    )
    password = fields.PasswordField("Password", validators=[validators.DataRequired()])
    submit = fields.SubmitField("Login")


BaseProfileForm = model_form(
    models.User,
    FlaskForm,
    field_args={
        "name": {"label": "Display Name"},
        "email": {"label": "Email"},
    },
    exclude=[
        "username",
        "password",
        "created_date",
        "updated_date",
        "is_active",
        "last_login_date",
    ],
)


class ProfileForm(BaseProfileForm):
    email = fields.StringField(
        "Email", validators=[validators.Email(), validators.Optional()]
    )
    favorite_types = fields.SelectMultipleField("Favorite Types of Restaurants", choices=TYPE_CORPUS)