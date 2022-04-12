import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase):  # класс по работе с новостями
    # для их обработки и хранения
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # заголовок новости
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # содержание новости
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)  # дата создания новости
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)  # показывать ли новость всем
    # или только автору

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')