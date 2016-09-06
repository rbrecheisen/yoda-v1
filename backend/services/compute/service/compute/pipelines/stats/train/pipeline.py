from celery import chord
from sklearn.cross_validation import StratifiedKFold
from service.compute.pipelines.util import get_access_token, get_storage_id_for_file
from service.compute.pipelines.base import Pipeline
from service.compute.pipelines.stats.train.tasks import run_training_fold, retrain_classifier


# ----------------------------------------------------------------------------------------------------------------------
class ClassifierTrainingPipeline(Pipeline):

    def run(self, params):

        # Validate the pipeline parameters
        self.validate_params(params)
        # Request access token from auth service
        token = get_access_token()
        # Get file storage ID from storage service
        storage_id = get_storage_id_for_file(params['file_id'], token)
        # Columns to exclude (optional parameter)
        exclude_columns = []
        if 'exclude_columns' in params.keys():
            exclude_columns = params['exclude_columns']

        # Create sub-task for each fold in the cross-validation
        header = []
        for train, test in StratifiedKFold(params['subject_labels'], n_folds=params['nr_folds'], shuffle=True):
            header.append(run_training_fold.subtask((
                storage_id, list(train), list(test), params['index_column'], params['target_column'],
                exclude_columns, token
            )))

        # Create final task to be executed when the fold tasks are finished
        body = retrain_classifier.subtask((
            storage_id, params['repository_id'], params['nr_folds'], params['index_column'],
            params['target_column'], exclude_columns, token
        ))

        # Create chord task consisting of a header listing each cross-validation fold and
        # a body task that averages the accuracies across folds and then retrains the classifier
        # using the optimal hyper-parameters
        job = chord(header=header, body=body)
        result = job.apply_async()
        return result.task_id

    @staticmethod
    def validate_params(params):

        assert 'file_id' in params.keys()
        assert params['file_id'] > 0
        assert 'subject_labels' in params.keys()
        assert len(params['subject_labels']) > 0
        assert 'index_column' in params.keys()
        assert 'target_column' in params.keys()
        assert 'nr_folds' in params.keys()
        assert params['nr_folds'] > 1
        assert 'classifier' in params.keys()
        assert params['classifier'] in ['svm-lin', 'svm-rbf']
        assert 'repository_id' in params.keys()
        assert params['repository_id'] > 0
