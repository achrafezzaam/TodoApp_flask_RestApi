from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    username = StringField('Enter a username', validators=[DataRequired()])
    password_1 = PasswordField('Enter a password', validators=[DataRequired()])
    password_2 = PasswordField('Retype your password', \
        validators=[DataRequired(),EqualTo('password_1')])
    submit = SubmitField('Create')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already in use. Try another one')