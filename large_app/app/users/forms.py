from flask_wtf import Form, RecaptchaField
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required, EqualTo, Email

class LoginForm(Form):
    email = TextField('Email address', [Required(), Email()])
    password = PasswordField('Password', [Required()])

class RegisterForm(Form):
    name = TextField('Nickname',[Required()])
    email = TextField('Email address', [Required(), Email()])
    password = PasswordField('Password', [Required()])
    confirm = PasswordField('Repeat Password', [
        Required(),
        EqualTo('password', message='Password must match')
    ])
    accept_tos = BooleanField('I accept the TOS',[Required()])
    recaptcha = RecaptchaField()
