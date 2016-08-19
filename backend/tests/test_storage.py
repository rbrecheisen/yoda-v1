import requests


def test_root():
    response = requests.get('http://192.168.99.107:8002')
    assert response.status_code == 200
