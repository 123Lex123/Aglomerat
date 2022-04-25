import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):  # модель пользователя, которая
    # содержит информацию о пользователях веб-приложения
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.Integer,
                                     default=datetime.datetime.now().timestamp)

    news = orm.relation("News", back_populates='user')  # связь таблиц пользователей и новостей

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):  # проверка на правильность введённого пароля
        return check_password_hash(self.hashed_password, password)
