from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired
from data import db_session
from data.category import Category


db_session.global_init('db/info.sqlite')
db_sess = db_session.create_session()
category = []
for id in range(10):
    category.append(db_sess.query(Category).get(id + 1))

class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    select_category = SelectField('Категория', choices=category)
    submit = SubmitField('Применить')