from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    select_category = SelectField('Категория', choices=[])
    submit = SubmitField('Применить')