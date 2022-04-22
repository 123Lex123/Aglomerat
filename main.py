from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.news import News
from data.category import Category
from forms.user import RegisterForm
from forms.login import LoginForm
from flask_login import LoginManager


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
    return render_template("index.html")


@app.route('/post')
def single_post():
    return render_template("single-post.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
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


def main():
    db_session.global_init("db/info.sqlite")

    user1 = User()
    user1.name = "Немой пользователь"
    user1.about = "Этот пользователь наслаждается тишиной."
    user1.email = "Mute@email.ru"
    user1.hashed_password = "qwerty"
    db_sess = db_session.create_session()
    db_sess.add(user1)
    db_sess.commit()

    user2 = User()
    user2.name = "Богдан"
    user2.about = "Журналист."
    user2.email = "Bogdan@email.ru"
    user2.hashed_password = "job123"
    db_sess.add(user2)

    user3 = User()
    user3.name = "Диванный критик"
    user3.about = "Знаю каждую новость и все пруфы на моей стороне."
    user3.email = "Сritic@email.ru"
    user3.hashed_password = "critic007"
    db_sess.add(user3)

    user4 = User()
    user4.name = "Алиса"
    user4.about = "Очень любознательная."
    user4.email = "Alice@yandex.ru"
    user4.hashed_password = "012345"
    db_sess.add(user4)

    db_sess.commit()

    category1 = Category(name="Культура")
    db_sess.add(category1)

    category2 = Category(name="Образование")
    db_sess.add(category2)

    category3 = Category(name="Спорт")
    db_sess.add(category3)

    category4 = Category(name="Другое")
    db_sess.add(category4)

    db_sess.commit()

    news1 = News(title="О наболевшем..", content="Чай 'беседа' стал не тот, что раньше!",
                 user_id=1)
    news1.categories.append(category4)
    db_sess.add(news1)

    news2 = News(title="Первая новость", content="Ура! Стажировка прошла успешно",
                 user_id=2)
    news2.categories.append(category4)
    db_sess.add(news2)

    news3 = News(title="Вторая новость", content="Завтра первый рабочий день. Пожелайте удачи!",
                 user_id=2)
    news3.categories.append(category4)
    db_sess.add(news3)

    news4 = News(title="Не проходи мимо", content="Вступайте в клуб, пока молодых "
                                                  "диванных критиков!",
                 user_id=3)
    news4.categories.append(category1)
    db_sess.add(news4)

    news5 = News(title="'Война и мир'", content="Не каждому удалось дойти до конца книги. "
                                                "Может его и вовсе нет?",
                 user_id=4)
    news5.categories.append(category2)
    db_sess.add(news5)

    db_sess.commit()

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()