import lib.http as http
from flask_restful import reqparse
from lib.authentication import token_required
from lib.resources import BaseResource
from service.compute.pipelines.base import PipelineRegistry
from service.compute.worker import run_pipeline, task_status, task_result
from service.compute.dao import TaskDao


# ----------------------------------------------------------------------------------------------------------------------
class RootResource(BaseResource):

    URI = '/'

    def get(self):
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
        
        # Add task ID, username and task status to arguments
        args['task_id'] = result.task_id
        args['status'] = task_status(result.task_id)
        args['username'] = self.current_user()['username']
        
        # Store task in database
        task_dao = TaskDao(self.db_session())
        task = task_dao.create(**args)

        return self.response(task.to_dict(), http.CREATED_201)


# ----------------------------------------------------------------------------------------------------------------------
class TaskResource(BaseResource):

    URI = '/tasks/{}'

    @token_required
    def get(self, id):
        # Get task from database
        task_dao = TaskDao(self.db_session())
        task = task_dao.retrieve(id=id)
        if task is None:
            return self.error_response('Task {} not found'.format(id), http.NOT_FOUND_404)
        # Get real-time status of the task
        status = task_status(task.task_id)
        # Save it in database
        task_dao = TaskDao(self.db_session())
        task.status = status
        task_dao.save(task)
        # If task completed successfully, we check its output type. If it's a string
        # then it's a sub-task ID and we retrieve the sub-task status. If it's a
        # dictionary we already have the end result and return it.
        # and check its status
        result = None
        if status == 'SUCCESS':
            result = task_result(task.task_id)
            if isinstance(result, dict):
                # Result is dictionary end result
                task.result = result
                task_dao.save(task)
                return self.response(task.to_dict())
            # Result is sub-task ID so retrieve its status
            sub_task_id = result
            status = task_status(sub_task_id)
            task.status = status
            # If sub-task completed successfully, we retrieve its results
            if status == 'SUCCESS':
                result = task_result(sub_task_id)
                task.result = result
            # Update status in database and set its result
            task_dao.save(task)
        return self.response(task.to_dict())

    @token_required
    def put(self, id):
        return self.response({})

    @token_required
    def delete(self, id):
        # TODO: explicitly cancel the task in the queue, then delete in database
        return self.response({}, http.NO_CONTENT_204)


# ----------------------------------------------------------------------------------------------------------------------
class PipelinesResource(BaseResource):

    URI = '/pipelines'

    @token_required
    def get(self):
        registry = PipelineRegistry()
        return self.response(registry.get_all())
