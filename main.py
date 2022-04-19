from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.news import News
from forms.user import RegisterForm
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


def main():
    db_session.global_init("db/info.sqlite")
    db_sess = db_session.create_session()
    #user1 = News()
    #user1.name = "Немой пользователь"
    #user1.about = "Этот пользователь наслаждается тишиной."
    #user1.email = "Mute@email.ru"
    #db_sess.add(user1)

    #user2 = User()
    #user2.name = "Богдан"
    #ser2.about = "Журналист."
    #user2.email = "Bogdan@email.ru"
    #db_sess.add(user2)

    #user3 = User()
    #user3.name = "Диванный критик"
    #user3.about = "Знаю каждую новость и все пруфы на моей стороне."
    #user3.email = "Сritic@email.ru"
    #db_sess.add(user3)

    #user4 = User()
    #user4.name = "Алиса"
    #user4.about = "Очень любознательная."
    #user4.email = "Alice@yandex.ru"
    #db_sess.add(user4)

    #news = News(title="О наболевшем..", content="Чай 'беседа' стал не тот, что раньше!",
    #            user_id=1, is_private=False)
    #db_sess.add(news)

    #news = News(title="Первая новость", content="Ура! Стажировка прошла успешно",
    #            user_id=2, is_private=False)
    #db_sess.add(news)

    #news = News(title="Вторая новость", content="Завтра первый рабочий день. Пожелайте удачи!",
    #            user_id=2, is_private=False)
    #db_sess.add(news)

    #news = News(title="Не проходи мимо", content="Вступайте в клуб, пока молодых "
    #                                             "диванных критиков!",
    #            user_id=3, is_private=False)
    #db_sess.add(news)

    #news = News(title="'Война и мир'", content="Не каждому удалось дойти до конца книги. "
    #                                           "Может его и вовсе нет?",
    #            user_id=4, is_private=False)
    #db_sess.add(news)

    #db_sess.commit()

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()