import random

from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.news import News
from data.category import Category
from forms.user import RegisterForm
from forms.login import LoginForm
from flask_login import LoginManager
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):  # получение вошедшего пользователя
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    news = sorted(news, key=lambda x: x.created_date, reverse=True)
    for x in news:
        x.created_date = datetime.date.fromtimestamp(x.created_date)

    return render_template("index.html", news=news)


@app.route('/post/<int:id>')
def single_post(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    rand_news = random.sample(news, 2)
    post = db_sess.query(News).get(id)

    author = post.user.name
    title = post.title
    text = post.content
    created_date = datetime.date.fromtimestamp(post.created_date)
    category = post.categories[0].name

    return render_template("single-post.html",
                           author=author, title=title,
                           text=text, created_date=created_date,
                           category=category, news=news, rand_news=rand_news)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/contact')
def contact():
    return render_template("base.html")


@app.route('/creators')
def creators():
    return render_template("base.html")


@app.route('/create_post')
def faq():
    return render_template("base.html")


def main():
    db_session.global_init("db/info.sqlite")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()