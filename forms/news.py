from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    set_category = IntegerField('Категория')
    submit = SubmitField('Применить')