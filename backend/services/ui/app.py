import os

from flask import Flask, redirect

from python.lib import init_env, uri

app = Flask(__name__, static_url_path='')


# --------------------------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    return app.send_static_file('index.html')


# --------------------------------------------------------------------------------------------------------------------
@app.route('/auth', methods=['GET'])
def auth():
    return redirect(uri('auth'))


# --------------------------------------------------------------------------------------------------------------------
@app.route('/auth/tokens', methods=['POST'])
def auth_tokens():
    return redirect(uri('auth', '/tokens'))


# --------------------------------------------------------------------------------------------------------------------
@app.route('/auth/token-checks', methods=['POST'])
def auth_token_checks():
    return redirect(uri('auth', '/token-checks'))


# --------------------------------------------------------------------------------------------------------------------
@app.route('/auth/users', methods=['GET', 'POST'])
def auth_users():
    return redirect(uri('auth', '/users'))


# --------------------------------------------------------------------------------------------------------------------
@app.route('/auth/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def auth_user(id):
    return redirect(uri('auth', '/users/{}'.format(id)))


# --------------------------------------------------------------------------------------------------------------------
@app.route('/auth/user-groups', methods=['GET', 'POST'])
def auth_user_groups():
    return redirect(uri('auth', '/user-groups'))


# --------------------------------------------------------------------------------------------------------------------
@app.route('/auth/user-groups/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def auth_user_group(id):
    return redirect(uri('auth', '/user-groups/{}'.format(id)))


# --------------------------------------------------------------------------------------------------------------------
@app.route('/auth/user-groups/<int:id>/users', methods=['GET'])
def auth_user_group_users(id):
    return redirect(uri('auth', '/user-groups/{}/users'.format(id)))


# --------------------------------------------------------------------------------------------------------------------
@app.route('/auth/user-groups/<int:id>/users/<int:user_id>', methods=['PUT', 'DELETE'])
def auth_user_group_user(id, user_id):
    return redirect(uri('auth', '/user-groups/{}/users/{}'.format(id, user_id)))


if __name__ == '__main__':
    init_env()
    host = os.getenv('UI_SERVICE_HOST')
    port = os.getenv('UI_SERVICE_PORT')
    port = int(port)
    app.run(host=host, port=port)
