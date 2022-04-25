import random
from data import news_api, users_api
from flask import Flask, render_template, redirect, make_response, jsonify
from data import db_session
from data.users import User
from data.news import News
from data.category import Category
from forms.news import NewsForm
from forms.user import RegisterForm
from forms.login import LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import datetime


db_session.global_init('db/info.sqlite')
db_sess = db_session.create_session()

all_news = db_sess.query(News).all()
list_date = []
for x in all_news:
    list_date.append([x, str(datetime.date.fromtimestamp(x.created_date))])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):  # получение вошедшего пользователя
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    news = list_date
    return render_template("index.html", news=news)


@app.route('/post/<int:id>')
def single_post(id):
    news = all_news
    rand_news = random.sample(news, 2)
    post = db_sess.query(News).get(id)

    author = post.user.name
    title = post.title
    text = post.content
    created_date = list_date[id - 1][1]
    category = "?"  # post.categories[0].name

    return render_template("single-post.html",
                           author=author, title=title,
                           text=text, created_date=created_date,
                           category=category, news=news, rand_news=rand_news)


@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = NewsForm()
    if form.validate_on_submit():
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        all_news = db_sess.query(News).all()
        list_date.append(
            [all_news[-1], str(datetime.date.fromtimestamp(all_news[-1].created_date))])
        return redirect('/')
    return render_template("add_post.html", title='Добавление новости', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    app.register_blueprint(news_api.blueprint, name='news_api')
    app.register_blueprint(users_api.blueprint, name='users_api')
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()