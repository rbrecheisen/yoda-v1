import json
import os

from flask import Flask, make_response, g
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import SimpleCache

from dao import FileTypeDao, ScanTypeDao, RepositoryDao
from models import FileType, ScanType
from lib.models import Base
from resources import (
    RootResource, FileTypesResource, ScanTypesResource,
    RepositoriesResource, RepositoryResource, UploadsResource, RepositoryFileResource, RepositoryFilesResource,
    RepositoryFileSetsResource, RepositoryFileSetResource, RepositoryFileSetFilesResource,
    RepositoryFileSetFileResource)

app = Flask(__name__)

if os.getenv('STORAGE_SERVICE_SETTINGS', None) is None:
    os.environ['STORAGE_SERVICE_SETTINGS'] = os.path.abspath('service/storage/settings.py')
app.config.from_envvar('STORAGE_SERVICE_SETTINGS')
print(app.config)

api = Api(app)
api.add_resource(RootResource, RootResource.URI)
api.add_resource(FileTypesResource, FileTypesResource.URI)
api.add_resource(ScanTypesResource, ScanTypesResource.URI)
api.add_resource(RepositoriesResource, RepositoriesResource.URI)
api.add_resource(RepositoryResource, RepositoryResource.URI.format('<int:id>'))
api.add_resource(UploadsResource, UploadsResource.URI)
api.add_resource(RepositoryFilesResource, RepositoryFilesResource.URI.format('<int:id>'))
api.add_resource(RepositoryFileResource, RepositoryFileResource.URI.format('<int:id>', '<int:file_id>'))
api.add_resource(RepositoryFileSetsResource, RepositoryFileSetsResource.URI.format('<int:id>'))
api.add_resource(RepositoryFileSetResource, RepositoryFileSetResource.URI.format('<int:id>', '<int:file_set_id>'))
api.add_resource(RepositoryFileSetFilesResource,
                 RepositoryFileSetFilesResource.URI.format('<int:id>', '<int:file_set_id>', '<int:file_id>'))
api.add_resource(RepositoryFileSetFileResource,
                 RepositoryFileSetFileResource.URI.format('<int:id>', '<int:file_set_id>', '<int:file_id>'))

db = SQLAlchemy(app)

cache = SimpleCache()


# ----------------------------------------------------------------------------------------------------------------------
def init_tables():
    # Create pre-defined file types
    file_type_dao = FileTypeDao(db.session)
    for name in FileType.ALL:
        file_type = file_type_dao.retrieve(name=name)
        if file_type is None:
            file_type_dao.create(name=name)
    # Create pre-defined scan types
    scan_type_dao = ScanTypeDao(db.session)
    for name in ScanType.ALL:
        scan_type = scan_type_dao.retrieve(name=name)
        if scan_type is None:
            scan_type_dao.create(name=name)
    # Create default repository
    repository_dao = RepositoryDao(db.session)
    repository = repository_dao.retrieve(name='default')
    if repository is None:
        repository_dao.create(name='default')


# ----------------------------------------------------------------------------------------------------------------------
@api.representation('application/json')
def output_json(data, code, headers=None):
    response = make_response(json.dumps(data), code)
    response.headers.extend(headers or {})
    return response


# ----------------------------------------------------------------------------------------------------------------------
@app.before_first_request
def init_db(drop=False):
    Base.query = db.session.query_property()
    if drop:
        Base.metadata.drop_all(db.engine)
    Base.metadata.create_all(bind=db.engine)
    init_tables()


# ----------------------------------------------------------------------------------------------------------------------
@app.before_request
def before_request():
    g.config = app.config
    g.db_session = db.session
    g.cache = cache


# ----------------------------------------------------------------------------------------------------------------------
@app.teardown_appcontext
def shutdown_database(e):
    db.session.remove()


if __name__ == '__main__':

    host = os.getenv('STORAGE_APP_SERVICE_HOST')
    port = os.getenv('STORAGE_APP_SERVICE_PORT')
    port = int(port)

    app.run(host=host, port=port)
