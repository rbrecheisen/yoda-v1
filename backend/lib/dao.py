from sqlalchemy.sql import func


# ----------------------------------------------------------------------------------------------------------------------
class BaseDao(object):

    def __init__(self, obj_class, db_session):
        self.obj_class = obj_class
        self.db_session = db_session

    def create(self, **kwargs):
        user_id = None
        if 'user_id' in kwargs.keys():
            user_id = kwargs['user_id']
            del kwargs['user_id']
        obj = self.obj_class(**kwargs)
        obj = self.save(obj, user_id)
        return obj

    def save(self, obj, user_id=None):
        if obj.id is None:
            obj.created_at = func.now()
            obj.created_by = user_id
        obj.updated_at = func.now()
        obj.updated_by = user_id
        self.db_session.add(obj)
        self.db_session.commit()
        return obj

    def retrieve(self, **kwargs):
        if 'id' in kwargs.keys():
            obj = self.obj_class.query.get(kwargs['id'])
        else:
            obj = self.obj_class.query.filter_by(**kwargs).first()
        return obj

    def retrieve_all(self, **kwargs):
        args = self.parse_args(**kwargs)
        if len(args.keys()) == 0:
            objects = self.obj_class.query.all()
        else:
            objects = self.obj_class.query.filter_by(**args).all()
        return objects

    def delete(self, obj):
        self.db_session.delete(obj)
        self.db_session.commit()

    @staticmethod
    def parse_args(**kwargs):
        args = {}
        for key in kwargs.keys():
            if kwargs[key]:
                args[key] = kwargs[key]
        return args
