import json
from flask import Flask, make_response

app = Flask(__name__, static_url_path='')

user = {
    'id': 1,
    'username': 'ralph',
    'email': 'ralph@yoda.com',
    'first_name': 'Ralph',
    'last_name': 'Brecheisen',
    'is_admin': True,
    'is_visible': True,
}


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')


@app.route('/auth/tokens', methods=['POST'])
def tokens():
    return make_response(
        json.dumps({'token': '1234', 'is_admin': True}), 201)


@app.route('/auth/users', methods=['GET'])
def get_users():
    return make_response(json.dumps([user]))


@app.route('/auth/users/<id>', methods=['GET'])
def get_user(id):
    return make_response(json.dumps(user))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
