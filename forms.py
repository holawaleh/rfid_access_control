from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])

class RFIDCardForm(FlaskForm):
    card_uid = StringField('Card UID', validators=[DataRequired()])
    user_id = SelectField('Assign to User', coerce=int, validators=[])
    description = TextAreaField('Description')
    is_active = BooleanField('Active', default=True)

class DoorForm(FlaskForm):
    name = StringField('Door Name', validators=[DataRequired()])
    location = StringField('Location')