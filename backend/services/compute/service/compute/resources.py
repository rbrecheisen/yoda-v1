import lib.http as http
from flask_restful import reqparse
from lib.resources import BaseResource
from lib.authentication import token_required
from service.compute.worker import run_task, get_task_status, get_task_result, cancel_task


# ----------------------------------------------------------------------------------------------------------------------
class RootResource(BaseResource):

    URI = '/'

    def get(self):
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
        parser.add_argument('duration', type=int, location='json')
        args = parser.parse_args()

        if args['duration'] is None:
            args['duration'] = 30

        result = run_task.apply_async((args['pipeline'], args['params'], args['duration']))

        return self.response({
            'id': result.task_id,
            'status': get_task_status(result.task_id),
        }, http.CREATED_201)


# ----------------------------------------------------------------------------------------------------------------------
class TaskResource(BaseResource):

    URI = '/tasks/{}'

    @token_required
    def get(self, id):
        return self.response({
            'status': get_task_status(id),
            'result': get_task_result(id),
        })

    @token_required
    def put(self, id):
        return self.response({})

    @token_required
    def delete(self, id):
        cancel_task(id)
        return self.response({}, http.NO_CONTENT_204)


# ----------------------------------------------------------------------------------------------------------------------
class PipelinesResource(BaseResource):

    URI = '/pipelines'
    pass
