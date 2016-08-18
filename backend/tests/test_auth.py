import requests


def uri(service, path=''):
    return 'http://{}:5000/{}'.format(service, path)


def test_root():
    response = requests.get(uri('auth'))
    assert response.status_code == 200
