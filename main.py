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


def main():
    db_session.global_init("db/info.sqlite")
    #user = User()
    #user.name = "Немой пользователь"
    #user.about = "Этот пользователь наслаждается тишиной."
    #user.email = "Mute@email.ru"
    #db_sess = db_session.create_session()
    #db_sess.add(user)
    #db_sess.commit()
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()