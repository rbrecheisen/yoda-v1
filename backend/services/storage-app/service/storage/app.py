import json
import os

from flask import Flask, make_response, g
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import SimpleCache

from dao import FileTypeDao, ScanTypeDao
from models import FileType, ScanType
from lib.models import Base
from lib.util import init_env
from resources import (
    RootResource, FileTypesResource, ScanTypesResource,
    RepositoriesResource, RepositoryResource, FilesResource, FileResource,
    FileSetsResource, FileSetResource, FileSetFilesResource, FileSetFileResource)

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
api.add_resource(FilesResource, FilesResource.URI)
api.add_resource(FileResource, FileResource.URI.format('<int:id>'))
api.add_resource(FileSetsResource, FileSetsResource.URI)
api.add_resource(FileSetResource, FileSetResource.URI.format('<int:id>'))
api.add_resource(FileSetFilesResource, FileSetFilesResource.URI.format('<int:id>'))
api.add_resource(FileSetFileResource, FileSetFileResource.URI.format('<int:id>', '<int:file_id>'))

db = SQLAlchemy(app)

cache = SimpleCache()


# ----------------------------------------------------------------------------------------------------------------------
def init_file_and_scan_types():
    file_type_dao = FileTypeDao(db.session)
    for name in FileType.ALL:
        file_type = file_type_dao.retrieve(name=name)
        if file_type is None:
            file_type_dao.create(name=name)
    scan_type_dao = ScanTypeDao(db.session)
    for name in ScanType.ALL:
        scan_type = scan_type_dao.retrieve(name=name)
        if scan_type is None:
            scan_type_dao.create(name=name)


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
    init_file_and_scan_types()


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
    init_env()
    host = os.getenv('STORAGE_APP_SERVICE_HOST')
    port = os.getenv('STORAGE_APP_SERVICE_PORT')
    port = int(port)
    app.run(host=host, port=port)
