import json
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from lib.models import BaseModel


class Task(BaseModel):
    
    __tablename__ = 'task'
    __mapper_args__ = {
        'polymorphic_identity': 'task',
    }

    # Task ID in database
    id = Column(Integer, ForeignKey('base.id'), primary_key=True)
    # Task ID as assigned by task queue
    task_id = Column(String, nullable=False, unique=True)
    # Task status
    status = Column(String, nullable=False)
    # Task result
    _result = Column(Text, nullable=True)
    # Name of pipeline associated with task
    pipeline_name = Column(String, nullable=False)
    # Parameters provided with task
    _params = Column(Text, nullable=False)
    # Username of user who submitted task. This is for lookup purposes only, given
    # that the USER table is only accessible to the auth service.
    username = Column(String, nullable=False)
    
    @property
    def params(self):
        return json.loads(self._params)
    
    @params.setter
    def params(self, params):
        self._params = json.dumps(params)
        
    @property
    def result(self):
        if self._result is None:
            return None
        return json.loads(self._result)
    
    @result.setter
    def result(self, result):
        self._result = json.dumps(result)

    def to_dict(self):
        obj = super(Task, self).to_dict()
        obj.update({
            'task_id': self.task_id,
            'status': self.status,
            'result': self.result,
            'pipeline_name': self.pipeline_name,
            'params': self.params,
            'username': self.username,
        })
        return obj
