from lib.dao import BaseDao
from models import User, UserGroup, Permission


# ----------------------------------------------------------------------------------------------------------------------
class UserDao(BaseDao):

    def __init__(self, db_session):
        super(UserDao, self).__init__(User, db_session)


# ----------------------------------------------------------------------------------------------------------------------
class UserGroupDao(BaseDao):

    def __init__(self, db_session):
        super(UserGroupDao, self).__init__(UserGroup, db_session)


# ----------------------------------------------------------------------------------------------------------------------
class PermissionDao(BaseDao):

    def __init__(self, db_session):
        super(PermissionDao, self).__init__(Permission, db_session)
