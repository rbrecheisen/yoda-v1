import requests
import os
import time
from util import uri, login_header, token_header, upload_file
from lib.util import generate_string


# --------------------------------------------------------------------------------------------------------------------
def test_root():
    response = requests.get(uri('compute'))
    assert response.status_code == 200


# --------------------------------------------------------------------------------------------------------------------
def test_train_classifier():

    if os.getenv('DATA_DIR', None) is None:
        return

    # Get access token
    response = requests.post(uri('auth', '/tokens'), headers=login_header('ralph', 'secret'))
    assert response.status_code == 201
    token = response.json()['token']

    # Create storage repository
    name = generate_string()
    response = requests.post(uri('storage', '/repositories'), headers=token_header(token), json={'name': name})
    assert response.status_code == 201
    repository_id = response.json()['id']

    # Get CSV file type ID
    response = requests.get(uri('storage', '/file-types?name=csv'), headers=token_header(token))
    assert response.status_code == 200
    file_type_id = response.json()[0]['id']

    # Get scan type ID
    response = requests.get(uri('storage', '/scan-types?name=none'), headers=token_header(token))
    assert response.status_code == 200
    scan_type_id = response.json()[0]['id']

    # Upload CSV file with brain features
    file_id = upload_file(
        os.path.join(os.getenv('DATA_DIR'), 'features_ext_multi_center.csv'),
        file_type_id, scan_type_id, repository_id, token)
    assert file_id

    # Train classifier using the uploaded CSV file
    response = requests.post(uri('compute', '/tasks'), headers=token_header(token), json={
        'pipeline_id': 1,
        'params': {
            'file_ids': [file_id],
            'classifier': {
                'name': 'svm-rbf',
            }
        }
    })
    assert response.status_code == 201
    task_id = response.json()['id']

    # Retrieve task status periodically until it finishes successfully. In practice,
    # this means the task status == SUCCESS and result != None
    while True:
        response = requests.get(uri('compute', '/tasks/{}'.format(task_id)), headers=token_header(token))
        assert response.status_code == 200
        status = response.json()['status']
        result = response.json()['result']
        print(status.lower())
        if status == 'SUCCESS' and result is not None:
            assert len(result) == 1
            break
        time.sleep(1)
