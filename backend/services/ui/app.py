import json
from flask import Flask, make_response, redirect

AUTH = 'http://0.0.0.0:5000'
COMPUTE = 'http://0.0.0.0:5001'
STORAGE = 'http://0.0.0.0:5002'

app = Flask(__name__, static_url_path='')


def output_json(data, code, headers=None):
    response = make_response(json.dumps(data), code)
    response.headers.extend(headers or {})
    return response


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/auth')
def auth():
    return redirect(AUTH)


@app.route('/auth/tokens')
def auth_tokens():
    return redirect('{}/tokens'.format(AUTH))


@app.route('/auth/token-checks')
def auth_token_checks():
    return redirect('{}/token-checks'.format(AUTH))


@app.route('/auth/users')
def auth_users():
    return redirect('{}/users'.format(AUTH))


@app.route('/auth/user-groups')
def auth_user_groups():
    return redirect('{}/user-groups'.format(AUTH))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
