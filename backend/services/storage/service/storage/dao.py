from lib.dao import BaseDao
from models import Repository, File, FileSet, FileType, ScanType


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryDao(BaseDao):

    def __init__(self, db_session):
        super(RepositoryDao, self).__init__(Repository, db_session)


# ----------------------------------------------------------------------------------------------------------------------
class FileDao(BaseDao):

    def __init__(self, db_session):
        super(FileDao, self).__init__(File, db_session)


# ----------------------------------------------------------------------------------------------------------------------
class FileSetDao(BaseDao):

    def __init__(self, db_session):
        super(FileSetDao, self).__init__(FileSet, db_session)


# ----------------------------------------------------------------------------------------------------------------------
class FileTypeDao(BaseDao):

    def __init__(self, db_session):
        super(FileTypeDao, self).__init__(FileType, db_session)


# ----------------------------------------------------------------------------------------------------------------------
class ScanTypeDao(BaseDao):

    def __init__(self, db_session):
        super(ScanTypeDao, self).__init__(ScanType, db_session)
