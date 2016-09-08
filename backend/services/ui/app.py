import json
from flask import Flask, make_response

app = Flask(__name__, static_url_path='')


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')


@app.route('/auth/tokens', methods=['POST'])
def tokens():
    return make_response(
        json.dumps({'token': '1234', 'is_admin': True}), 201)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
