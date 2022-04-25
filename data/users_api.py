import flask
from . import db_session
from .users import User
from flask import jsonify

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'name', 'about', 'email', 'created_date'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    got_user = db_sess.query(User).get(user_id)
    if not got_user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': got_user.to_dict(only=('id', 'name', 'about', 'email', 'created_date'))
        }
    )