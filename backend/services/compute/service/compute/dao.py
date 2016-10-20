from models import Task
from lib.dao import BaseDao


class TaskDao(BaseDao):
    
    def __init__(self, db_session):
        super(TaskDao, self).__init__(Task, db_session)
