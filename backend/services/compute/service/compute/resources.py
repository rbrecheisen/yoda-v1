import lib.http as http
from flask_restful import reqparse
from lib.resources import BaseResource
from lib.authentication import token_required
from service.compute.worker import run_smoothing_pipeline, task_status, task_result


# ----------------------------------------------------------------------------------------------------------------------
class RootResource(BaseResource):

    URI = '/'

    def get(self):
        print('Returning root endpoint...')
        return self.response({
            'service': 'compute',
            'endpoints': ['tasks', 'pipelines', 'task-results'],
        })


# ----------------------------------------------------------------------------------------------------------------------
class TasksResource(BaseResource):

    URI = '/tasks'

    @token_required
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('pipeline', type=int, required=True, location='json')
        parser.add_argument('params', type=dict, required=True, location='json')
        args = parser.parse_args()

        result = run_smoothing_pipeline.apply_async((args['params'],))

        return self.response({
            'id': result.task_id,
            'status': task_status(run_smoothing_pipeline, result.task_id),
        }, http.CREATED_201)


# ----------------------------------------------------------------------------------------------------------------------
class TaskResource(BaseResource):

    URI = '/tasks/{}'

    @token_required
    def get(self, id):
        return self.response({
            'status': task_status(run_smoothing_pipeline, id),
            'result': task_result(run_smoothing_pipeline, id),
        })

    @token_required
    def put(self, id):
        return self.response({})

    @token_required
    def delete(self, id):
        return self.response({}, http.NO_CONTENT_204)


# ----------------------------------------------------------------------------------------------------------------------
class PipelinesResource(BaseResource):

    URI = '/pipelines'
    pass
