import json
from flask import Flask, make_response
from flask_restful import Api, Resource
from flask_restful import reqparse

app = Flask(__name__, static_url_path='')
api = Api(app)

users = list()
users.append({
    'id': 1,
    'username': 'ralph',
    'email': 'ralph@yoda.com',
    'first_name': 'Ralph',
    'last_name': 'Brecheisen',
    'is_superuser': True,
    'is_admin': True,
    'is_active': True,
    'is_visible': True,
})


class IndexResource(Resource):
    def get(self):
        return app.send_static_file('index.html')


class TokensResource(Resource):
    def post(self):
        return make_response(json.dumps({'token': '1234', 'is_admin': True}), 201)


class UsersResource(Resource):

    def get(self):
        return make_response(json.dumps(users))

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('password', type=str, location='json')
        parser.add_argument('email', type=str, location='json')
        parser.add_argument('first_name', type=str, location='json')
        parser.add_argument('last_name', type=str, location='json')
        parser.add_argument('is_admin', type=bool, location='json')
        parser.add_argument('is_active', type=bool, location='json')
        args = parser.parse_args()
        users.append({
            'id': users[len(users) - 1]['id'] + 1,
            'username': args['username'],
            'email': args['email'],
            'first_name': args['first_name'],
            'last_name': args['last_name'],
            'is_admin': args['is_admin'],
            'is_active': args['is_active'],
            'is_visible': True})
        return make_response(json.dumps(users[len(users) - 1]), 201)


class UserResource(Resource):

    def get(self, id):
        return make_response(json.dumps(users[id - 1]))

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('password', type=str, location='json')
        parser.add_argument('email', type=str, location='json')
        parser.add_argument('first_name', type=str, location='json')
        parser.add_argument('last_name', type=str, location='json')
        parser.add_argument('is_admin', type=bool, location='json')
        parser.add_argument('is_active', type=bool, location='json')
        args = parser.parse_args()

        print(args.get('username'))

        users[id - 1]['username'] = args['username']
        users[id - 1]['password'] = args['password']
        users[id - 1]['email'] = args['email']
        users[id - 1]['first_name'] = args['first_name']
        users[id - 1]['last_name'] = args['last_name']
        users[id - 1]['is_admin'] = args['is_admin']
        users[id - 1]['is_active'] = args['is_active']
        return make_response(json.dumps(users[id - 1]), 200)


api.add_resource(IndexResource, '/')
api.add_resource(TokensResource, '/auth/tokens')
api.add_resource(UsersResource, '/auth/users')
api.add_resource(UserResource, '/auth/users/<int:id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
