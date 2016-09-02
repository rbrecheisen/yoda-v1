from celery import chord
from sklearn.cross_validation import StratifiedKFold
from service.compute.pipelines.base import Pipeline
from service.compute.pipelines.util import get_access_token, get_storage_id_for_file
from service.compute.pipelines.stats.train.tasks import run_training_fold, retrain_classifier


# ----------------------------------------------------------------------------------------------------------------------
class ClassifierTrainingPipeline(Pipeline):

    def run(self, params):

        print('run_training_fold: {}'.format(run_training_fold))
        print('retrain_classifier: {}'.format(retrain_classifier))

        header = []
        for i in range(2):
            header.append(run_training_fold.subtask({
                'storage_id': 'flaskdjflkdjsfasd',
                'train': [],
                'test': [],
                'index_column': 'MRid',
                'target_column': 'Diagnosis',
                'exclude_columns': ['Gender', 'Center'],
                'token': 'kldjflkasdjfasldkfj',
            }))

        body = retrain_classifier.subtask({
            'storage_id': 'salfkjsadflksjad',
            'repository_id': 1,
            'nr_folds': 2,
            'index_column': 'MRid',
            'target_column': 'Diagnosis',
            'exclude_columns': ['Gender', 'Center'],
            'token': 'lkjdsalkfjadslkfjds',
        })

        # # Validate the pipeline parameters
        # self.validate_params(params)
        # # Request access token from auth service
        # token = get_access_token()
        # # Get file storage ID from storage service
        # storage_id = get_storage_id_for_file(params['file_id'], token)
        # # Columns to exclude (optional parameter)
        # exclude_columns = []
        # if 'exclude_columns' in params.keys():
        #     exclude_columns = params['exclude_columns']
        #
        # # Create sub-task for each fold in the cross-validation
        # header = []
        # for train, test in StratifiedKFold(params['subject_labels'], n_folds=params['nr_folds'], shuffle=True):
        #     header.append(run_training_fold.subtask(
        #         storage_id=storage_id,
        #         train=list(train),
        #         test=list(test),
        #         index_column=params['index_column'],
        #         target_column=params['target_column'],
        #         exclude_columns=exclude_columns,
        #         token=token,
        #     ))
        #
        # # Create final task to be executed when the fold tasks are finished
        # body = retrain_classifier.subtask(
        #     storage_id=storage_id,
        #     repository_id=params['repository_id'],
        #     nr_folds=params['nr_folds'],
        #     index_column=params['index_column'],
        #     target_column=params['target_column'],
        #     exlude_columns=exclude_columns,
        #     token=token,
        # )

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
