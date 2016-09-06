import os
import tarfile
import requests
import pandas as pd
from sklearn.externals import joblib
from lib.util import service_uri, generate_string
from lib.authentication import token_header
from lib.files import upload_file


# ----------------------------------------------------------------------------------------------------------------------
def load_features(file_path, **kwargs):
    features = pd.read_csv(file_path, **kwargs)
    return features


# ----------------------------------------------------------------------------------------------------------------------
def load_features_for(file_path, target_column, values, **kwargs):
    features = load_features(file_path, **kwargs)
    tmp = []
    for i in range(len(values)):
        tmp.append(features[features[target_column] == values[i]])
    return pd.concat(tmp)


# ----------------------------------------------------------------------------------------------------------------------
def get_xy(features, target_column=None, exclude_columns=list()):
    predictors = list(features.columns)
    for column in exclude_columns:
        if column in predictors:
            predictors.remove(column)
    if target_column:
        if target_column not in exclude_columns:
            if target_column in predictors:
                predictors.remove(target_column)
    X = features[predictors]
    X = X.as_matrix()
    if target_column:
        y = features[target_column]
        y = y.as_matrix()
    else:
        y = None
    return X, y


# ----------------------------------------------------------------------------------------------------------------------
def save_model(model, target_dir):
    file_name = generate_string()
    file_path = os.path.join(target_dir, file_name)
    joblib.dump(model, file_path)
    arch_path = '{}.tar.gz'.format(file_path)
    arch_file = tarfile.open(arch_path, 'w:gz')
    for f in os.listdir(target_dir):
        if f.startswith(file_name):
            # We add each file based on its full file path but we specify the archive file
            # name to be just the file name (without its path). When we unpack the archive
            # later this will prevent subdirectories from being created.
            arch_file.add(os.path.join(target_dir, f), arcname=f)
    arch_file.close()
    return arch_path


# ----------------------------------------------------------------------------------------------------------------------
def load_model(file_path):
    # We unpack the archive file to a sub-directory so we can easily search
    # for the model's main file
    dir_name = os.path.join(os.path.dirname(file_path), 'model')
    arch_file = tarfile.open(file_path, 'r:gz')
    arch_file.extractall(dir_name)
    arch_file.close()
    # Search for main model file
    main_file = None
    for f in os.listdir(dir_name):
        if not f.endswith('.npy'):
            main_file = os.path.join(dir_name, f)
            break
    if main_file is None:
        raise RuntimeError('Could not find model main file')
    model = joblib.load(main_file)
    return model


# ----------------------------------------------------------------------------------------------------------------------
def upload_model_archive(file_path, repository_id, token):
    response = requests.get('{}/file-types?name=binary'.format(service_uri('storage')), headers=token_header(token))
    file_type_id = response.json()[0]['id']
    response = requests.get('{}/scan-types?name=none'.format(service_uri('storage')), headers=token_header(token))
    scan_type_id = response.json()[0]['id']
    try:
        _, storage_id = upload_file(file_path, file_type_id, scan_type_id, repository_id, token)
        return storage_id
    except RuntimeError as e:
        print('Failed to upload model ({})'.format(e.message))
