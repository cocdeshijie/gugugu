from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Group, User

class DeleteGroupForm(FlaskForm):
    group_id = HiddenField()

class CreateGroupForm(FlaskForm):
    pass