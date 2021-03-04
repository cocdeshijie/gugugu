from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional


class DeleteGroupForm(FlaskForm):
    group_id = HiddenField()


class CreateGroupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    space_limit = IntegerField('Space limit', default=536870912, validators=[Optional()])
    create = SubmitField('Create')
