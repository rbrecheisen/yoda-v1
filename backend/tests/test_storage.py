import requests
from util import uri, login_header, token_header


def test_root():
    response = requests.get(uri('storage'))
    assert response.status_code == 200
    pass
