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
    username = StringField('Username',
                           validators=[Optional()])
    email = StringField('Email',
                        validators=[Optional()])
    old_password = PasswordField('Old password',
                                 validators=[Optional()])
    new_password = PasswordField('New password',
                                 validators=[Optional(),
                                             EqualTo('new_password_confirm',
                                                     message='Password does not match.')])
    new_password_confirm = PasswordField('New password',
                                         validators=[Optional()])
    submit = SubmitField('Submit')

    def check_username(self):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('Username is in use.')