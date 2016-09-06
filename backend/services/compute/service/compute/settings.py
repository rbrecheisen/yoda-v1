import os
import logging

# ------------------------------------------------------------------------------------------------------------------
# Log settings
# ------------------------------------------------------------------------------------------------------------------

formatter = logging.Formatter('%(asctime)s - [%(levelname)s] %(message)s')

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# ------------------------------------------------------------------------------------------------------------------
# Flask settings
# ------------------------------------------------------------------------------------------------------------------

PROPAGATE_EXCEPTIONS = True
RESTFUL_JSON = {'indent': 2, 'sort_keys': True}

# ------------------------------------------------------------------------------------------------------------------
# Celery settings
# ------------------------------------------------------------------------------------------------------------------

BROKER_URL = os.getenv('BROKER_URL', 'redis://localhost:6379/0')

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_CHORD_PROPAGATES = True

# ------------------------------------------------------------------------------------------------------------------
# Pipelines
# ------------------------------------------------------------------------------------------------------------------

PIPELINES = {
    'svm_train': {
        'display_name': 'Support Vector Machine (Training)',
        'module_path': 'service.compute.pipelines.stats.train.classification',
        'tasks_module_path': 'service.compute.pipelines.stats.train.classification',
        'class_name': 'ClassifierTrainingPipeline',
        'params': {
            'file_id': {'type': 'int', 'min_value': 1},
            'subject_labels': {'type': 'str_list', 'min_length': 10},
            'nr_folds': {'type': 'int', 'min_value': 2, 'default': 10},
            'index_column': {'type': 'str'},
            'target_column': {'type': 'str'},
            'excluded_columns': {'type': 'str_list', 'default': []},
            'kernel': {'type': 'str', 'allowed_values': ['linear', 'rbf', 'poly'], 'default': 'rbf'},
            'repository_id': {'type': 'int', 'min_value': 1},
        },
        'outputs': {
            'accuracy': {'type': 'int'},
            'C': {'type': 'float'},
            'gamma': {'type': 'float'},
            'classifier_id': {'type': 'str'},
        },
    },
    'svm_predict': {
        'display_name': 'Support Vector Machine (Prediction)',
        'module_path': 'service.compute.pipelines.stats.predict.classification',
        'tasks_module_path': 'service.compute.pipelines.stats.predict.classification',
        'class_name': 'ClassifierPredictionPipeline',
        'params': {},
        'outputs': {},
    },
}

# ------------------------------------------------------------------------------------------------------------------
# Security settings
# ------------------------------------------------------------------------------------------------------------------
WORKER_USERNAME = 'worker'
WORKER_PASSWORD = 'secret'
