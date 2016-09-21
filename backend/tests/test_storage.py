import os
import requests
from util import uri
from lib.util import generate_string
from lib.authentication import login_header, token_header
from lib.files import upload_file
from util import service_uri


# --------------------------------------------------------------------------------------------------------------------
def test_root():
    response = requests.get(uri('storage'))
    assert response.status_code == 200
    pass


# --------------------------------------------------------------------------------------------------------------------
def test_upload_and_download():

    if os.getenv('DATA_DIR', None) is None:
        return

    response = requests.post('{}/tokens'.format(service_uri('auth')), headers=login_header('ralph', 'secret'))
    assert response.status_code == 201
    token = response.json()['token']

    response = requests.get('{}/file-types?name=txt'.format(service_uri('storage')), headers=token_header(token))
    assert response.status_code == 200
    file_type_id = response.json()[0]['id']

    response = requests.get('{}/scan-types?name=none'.format(service_uri('storage')), headers=token_header(token))
    assert response.status_code == 200
    scan_type_id = response.json()[0]['id']

    name = generate_string()
    response = requests.post('{}/repositories'.format(service_uri('storage')), json={'name': name}, headers=token_header(token))
    assert response.status_code == 201
    repository_id = response.json()['id']

    file_name = os.path.join(os.getenv('DATA_DIR'), 'data.nii.gz')
    file_id, _ = upload_file(file_name, file_type_id, scan_type_id, repository_id, token)

    response = requests.get('{}/files/{}'.format(service_uri('storage'), file_id), headers=token_header(token))
    assert response.status_code == 200
    storage_id = response.json()['storage_id']

    response = requests.get('{}/downloads/{}'.format(service_uri('storage'), storage_id), headers=token_header(token))
    assert response.status_code == 200
    assert response.content

    with open('tmp.nii.gz', 'wb') as f:
        for chunk in response.iter_content(1024 * 1024):
            f.write(chunk)

    n = os.path.getsize('tmp.nii.gz')
    m = os.path.getsize(file_name)
    assert n == m

    os.system('rm -f tmp.nii.gz')


# --------------------------------------------------------------------------------------------------------------------
def test_resume_upload():

    if os.getenv('DATA_DIR', None) is None:
        return


# # --------------------------------------------------------------------------------------------------------------------
# def test_upload_to_amazon():
#
#     if os.getenv('DATA_DIR', None) is None:
#         return
#
#     with open(os.path.join(os.getenv('DATA_DIR'), 'data.nii.gz'), 'rb') as f:
#         response = requests.put(
#             '{}/s3files/{}'.format(service_uri('storage'), 'data.nii.gz'), files={'file': f})
#         print(response.content)
