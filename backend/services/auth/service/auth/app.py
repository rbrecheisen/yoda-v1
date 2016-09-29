import json
import os

from flask import Flask, make_response, g
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from dao import UserDao
from lib.models import Base
from resources import (
    RootResource, TokensResource, TokenChecksResource, UsersResource, UserResource, UserGroupsResource,
    UserGroupResource, UserGroupUsersResource, UserGroupUserResource)

app = Flask(__name__)

if os.getenv('AUTH_SERVICE_SETTINGS', None) is None:
    os.environ['AUTH_SERVICE_SETTINGS'] = os.path.abspath('service/auth/settings.py')
app.config.from_envvar('AUTH_SERVICE_SETTINGS')
print(app.config)

api = Api(app)
api.add_resource(RootResource, RootResource.URI)
api.add_resource(TokensResource, TokensResource.URI)
api.add_resource(TokenChecksResource, TokenChecksResource.URI)
api.add_resource(UsersResource, UsersResource.URI)
api.add_resource(UserResource, UserResource.URI.format('<int:id>'))
api.add_resource(UserGroupsResource, UserGroupsResource.URI)
api.add_resource(UserGroupResource, UserGroupResource.URI.format('<int:id>'))
api.add_resource(UserGroupUsersResource, UserGroupUsersResource.URI.format('<int:id>'))
api.add_resource(UserGroupUserResource, UserGroupUserResource.URI.format('<int:id>', '<int:user_id>'))

db = SQLAlchemy(app)


# ----------------------------------------------------------------------------------------------------------------------
def init_users():
    user_dao = UserDao(db.session)
    for item in app.config['USERS']:
        user = user_dao.retrieve(username=item['username'])
        if user is None:
            user_dao.create(
                username=item['username'],
                password=item['password'],
                email=item['email'],
                first_name=item['first_name'],
                last_name=item['last_name'],
                is_superuser=item['is_superuser'],
                is_admin=item['is_admin'],
                is_active=item['is_active'],
                is_visible=item['is_visible'])


# ----------------------------------------------------------------------------------------------------------------------
@api.representation('application/json')
def output_json(data, code, headers=None):
    response = make_response(json.dumps(data), code)
    response.headers.extend(headers or {})
    return response


# ----------------------------------------------------------------------------------------------------------------------
@app.before_first_request
def init_db(drop=False):
    Base.query = db.session.query_property()
    if drop:
        print('Dropping tables...')
        Base.metadata.drop_all(db.engine)
    Base.metadata.create_all(bind=db.engine)
    init_users()


# ----------------------------------------------------------------------------------------------------------------------
@app.before_request
def before_request():
    g.config = app.config
    g.db_session = db.session


# ----------------------------------------------------------------------------------------------------------------------
@app.teardown_appcontext
def shutdown_database(e):
    db.session.remove()


if __name__ == '__main__':

    host = os.getenv('AUTH_SERVICE_HOST')
    port = os.getenv('AUTH_SERVICE_PORT')
    port = int(port)

    app.run(host=host, port=port)
