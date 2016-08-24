import lib.http as http
from flask_restful import reqparse, request
from lib.resources import BaseResource
from dao import UserDao
from authentication import create_token, check_token, login_required, token_required


# ----------------------------------------------------------------------------------------------------------------------
class RootResource(BaseResource):

    URI = '/'

    def get(self):
        return self.response({
            'service': 'auth',
            'endpoints': ['tokens', 'token-checks', 'users']
        })


# ----------------------------------------------------------------------------------------------------------------------
class TokensResource(BaseResource):

    URI = '/tokens'

    @login_required
    def post(self):

        user = self.current_user()
        if user is None:
            msg = 'User not signed in'
            return self.error_response(msg, http.FORBIDDEN_403)
        token, msg = create_token(user)
        if token is None:
            return self.error_response(msg, http.INTERNAL_SERVER_ERROR_500)
        return self.response({
            'token': token,
            'is_admin': user.is_admin,
        }, http.CREATED_201)


# ----------------------------------------------------------------------------------------------------------------------
class TokenChecksResource(BaseResource):

    URI = '/token-checks'

    def post(self):

        auth = request.authorization
        if auth is None:
            msg = 'Missing token'
            return self.error_response(msg, http.FORBIDDEN_403)
        user, msg = check_token(auth.username)
        if user is None:
            return self.error_response(msg, http.FORBIDDEN_403)
        return self.response({
            'user': user.to_dict()
        }, http.CREATED_201)


# ----------------------------------------------------------------------------------------------------------------------
class UsersResource(BaseResource):

    URI = '/users'

    @token_required
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='args')
        parser.add_argument('email', type=str, location='args')
        parser.add_argument('first_name', type=str, location='args')
        parser.add_argument('last_name', type=str, location='args')
        parser.add_argument('is_admin', type=bool, location='args')
        parser.add_argument('is_active', type=bool, location='args')
        args = parser.parse_args()

        user_dao = UserDao(self.db_session())
        users = user_dao.retrieve_all(**args)
        result = [user.to_dict() for user in users]

        return self.response(result)

    @token_required
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, location='json')
        parser.add_argument('password', type=str, required=True, location='json')
        parser.add_argument('email', type=str, required=True, location='json')
        parser.add_argument('first_name', type=str, location='json')
        parser.add_argument('last_name', type=str, location='json')
        parser.add_argument('is_admin', type=bool, location='json')
        parser.add_argument('is_active', type=bool, location='json')
        args = parser.parse_args()

        user_dao = UserDao(self.db_session())
        user = user_dao.create(**args)

        return self.response(user.to_dict(), http.CREATED_201)


# ----------------------------------------------------------------------------------------------------------------------
class UserResource(BaseResource):

    URI = '/users/{}'

    @token_required
    def get(self, id):
        return self.response({})

    @token_required
    def put(self, id):
        return self.response({})

    @token_required
    def delete(self, id):
        return self.response({}, http.NO_CONTENT_204)
