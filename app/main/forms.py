from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, IntegerField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Optional, EqualTo
from ..models import User

class DeleteGroupForm(FlaskForm):
    group_id = HiddenField()


class CreateGroupForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired()])
    space_limit = IntegerField('Space limit',
                               default=536870912,
                               validators=[Optional()])
    create = SubmitField('Create')


class UserAccountForm(FlaskForm):
    username = StringField('Username')
    email = StringField('Email')
    old_password = PasswordField('Old password')
    new_password = PasswordField('New password',
                                 validators=[EqualTo('new_password_confirm', message='Password does not match.')])
    new_password_confirm = PasswordField('New password')

    def check_username(self):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('Username is in use.')