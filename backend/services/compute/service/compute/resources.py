import lib.http as http
from flask_restful import reqparse
from lib.resources import BaseResource
from lib.authentication import token_required
from service.compute.worker import run_pipeline, task_status, task_result


# ----------------------------------------------------------------------------------------------------------------------
class RootResource(BaseResource):

    URI = '/'

    def get(self):
        print('Returning root endpoint...')
        return self.response({
            'service': 'compute',
            'endpoints': ['tasks', 'pipelines'],
        })


# ----------------------------------------------------------------------------------------------------------------------
class TasksResource(BaseResource):

    URI = '/tasks'

    @token_required
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('pipeline_name', type=str, required=True, location='json')
        parser.add_argument('params', type=dict, required=True, location='json')
        args = parser.parse_args()

        result = run_pipeline.apply_async((args['pipeline_name'], args['params']))

        return self.response({
            'id': result.task_id,
            'status': task_status(result.task_id),
        }, http.CREATED_201)


# ----------------------------------------------------------------------------------------------------------------------
class TaskResource(BaseResource):

    URI = '/tasks/{}'

    @token_required
    def get(self, id):
        # Get status of the task
        status = task_status(id)
        result = None
        # If task completed successfully, we check its output type. If it's a string
        # then it's a sub-task ID and we retrieve the sub-task status. If it's a
        # dictionary we already have the end result and return it.
        # and check its status
        if status == 'SUCCESS':
            result = task_result(id)
            if isinstance(result, dict):
                # Result is dictionary end result
                return self.response({'status': status, 'result': result})
            # Result is sub-task ID so retrieve its status
            sub_task_id = result
            status = task_status(sub_task_id)
            result = None
            # If sub-task completed successfully, we retrieve its results
            if status == 'SUCCESS':
                result = task_result(sub_task_id)
        return self.response({'status': status, 'result': result})

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
