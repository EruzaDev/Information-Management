from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, DecimalField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional

class AdminLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AdminChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

class GameForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    release_year = IntegerField('Release Year', validators=[Optional(), NumberRange(min=1950, max=2100)])
    description = TextAreaField('Description', validators=[Optional()])
    stock_quantity = IntegerField('Stock Quantity', validators=[DataRequired(), NumberRange(min=0)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    image_url = StringField('Image URL', validators=[Optional(), Length(max=255)])
    genre_id = SelectField('Genre', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')


class GenreForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Submit')

class EmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    position = StringField('Position', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    role = StringField('Role', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Submit')

class CustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    address = StringField('Address', validators=[Optional(), Length(max=255)])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    submit = SubmitField('Submit')