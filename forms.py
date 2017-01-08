from flask_wtf import FlaskForm

from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import URLField

from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, \
    url, ValidationError

from models import User


class BookmarkForm(FlaskForm):
    url = URLField('The URL for your bookmark:', validators=[DataRequired(), url()])
    description = StringField('Add an optional description:')

    def validate(self):
        if not self.url.data.startswith("http://") or \
                self.url.data.startswith("https://"):
            self.url.data = "http://" + self.url.data

        # Call built-in validators
        if not FlaskForm.validate(self):
            return False

        # If no description was provided, set description to URL
        if not self.description.data:
            self.description.data = self.url.data

        return True


class LoginForm(FlaskForm):
    username = StringField("Your username:", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Log in")  # Put here to demonstrate that WTForms can generate button


class SignupForm(FlaskForm):
    username = StringField('Username',
                           validators=[
                               DataRequired(), Length(3, 80),
                               Regexp('^[A-Za-z0-9_]{3,}$',
                                      message='User names consist of numbers, letters,'
                                              'and underscores.')])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 120), Email()])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There already is a user with this email address.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')
