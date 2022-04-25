import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase, SerializerMixin):  # класс по работе с новостями
    # для их обработки и хранения
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # заголовок новости
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # содержание новости
    created_date = sqlalchemy.Column(sqlalchemy.Integer,
                                     default=datetime.datetime.now().timestamp)  # дата создания новости

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    categories = orm.relation("Category",
                              secondary="association",
                              backref="news")