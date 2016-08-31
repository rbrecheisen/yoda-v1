import requests
import os
import time
import sys
import pandas as pd
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

    # Load features and extract HC and SZ subjects
    file_path = os.path.join(os.getenv('DATA_DIR'), 'features_ext_multi_center.csv')
    features = pd.read_csv(file_path, index_col='MRid')
    tmp = []
    for label in ['HC', 'SZ']:
        tmp.append(features[features['Diagnosis'] == label])
    features = pd.concat(tmp)
    features.to_csv('/tmp/features.csv', index=True, index_label='MRid')
    subject_labels = list(features['Diagnosis'])

    # Upload CSV file with brain features
    file_id = upload_file('/tmp/features.csv', file_type_id, scan_type_id, repository_id, token)
    assert file_id

    # Delete temporary features file
    os.system('rm -f /tmp/features.csv')

    # Train classifier using the uploaded CSV file. As parameters we specify the
    # pipeline ID (which in this case is a classifier training pipeline). The 'file_id'
    # refers to the CSV file. The parameter 'subject_labels' contains a list of diagnostic
    # labels. This list is used to pre-calculate training and testing indices which can be
    # passed to the different workers handling the cross-validation folds in parallel.
    response = requests.post(uri('compute', '/tasks'), headers=token_header(token), json={
        'pipeline_id': 1,
        'params': {
            'file_id': file_id,
            'subject_labels': subject_labels,
            'nr_folds': 2,
            'index_column': 'MRid',
            'target_column': 'Diagnosis',
            'exclude_columns': ['Gender', 'Center'],
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
        assert status == 'PENDING' or status == 'SUCCESS'
        result = response.json()['result']
        sys.stdout.write('.')
        sys.stdout.flush()
        if status == 'SUCCESS' and result is not None:
            print(result)
            break
        time.sleep(2)
