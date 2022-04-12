from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.fields import EmailField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):  # класс, отвечающий за вход в учётную запись
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')