import logging
import os
import lib.http as http
from flask import make_response
from flask_restful import reqparse
from lib.resources import BaseResource
from lib.authentication import token_required
from dao import FileDao, FileTypeDao, ScanTypeDao, RepositoryDao, FileSetDao

LOG = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------------------------------------
class RootResource(BaseResource):

    URI = '/'

    def get(self):
        return {
            'service': 'storage',
            'endpoints': ['file-types', 'scan-types', 'repositories', 'files', 'file-sets'],
        }


# ----------------------------------------------------------------------------------------------------------------------
class FileTypesResource(BaseResource):

    URI = '/file-types'

    @token_required
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='args')
        args = parser.parse_args()

        file_type_dao = FileTypeDao(self.db_session())
        file_types = file_type_dao.retrieve_all(**args)
        result = [file_type.to_dict() for file_type in file_types]

        return result, http.OK_200


# ----------------------------------------------------------------------------------------------------------------------
class ScanTypesResource(BaseResource):

    URI = '/scan-types'

    @token_required
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='args')
        args = parser.parse_args()

        scan_type_dao = ScanTypeDao(self.db_session())
        scan_types = scan_type_dao.retrieve_all(**args)
        result = [scan_type.to_dict() for scan_type in scan_types]

        return result, http.OK_200


# ----------------------------------------------------------------------------------------------------------------------
class RepositoriesResource(BaseResource):

    URI = '/repositories'

    @token_required
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='args')
        args = parser.parse_args()

        repository_dao = RepositoryDao(self.db_session())
        repositories = repository_dao.retrieve_all(**args)
        result = [repository.to_dict() for repository in repositories]

        return result, http.OK_200

    @token_required
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        args = parser.parse_args()

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.create(**args)

        return repository.to_dict(), http.CREATED_201


# ----------------------------------------------------------------------------------------------------------------------
class RepositoryResource(BaseResource):

    URI = '/repositories/{}'

    @token_required
    def get(self, id):

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)

        return repository.to_dict(), http.OK_200

    @token_required
    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        args = parser.parse_args()

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)
        repository.name = args['name']
        repository_dao.save(repository)

        return repository.to_dict(), http.OK_200

    @token_required
    def delete(self, id):

        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=id)
        repository_dao.delete(repository)

        return {}, http.NO_CONTENT_204


# ----------------------------------------------------------------------------------------------------------------------
class FilesResource(BaseResource):

    URI = '/files'

    @token_required
    def get(self):

        # This method will only get called by Nginx to pre-authorize file uploads.
        # We should perform a permission check and return the result.
        return {}, http.OK_200

    @token_required
    def post(self):

        # These arguments are posted by nginx-big-upload as form encoded data
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, location='form')
        parser.add_argument('path', type=str, location='form')
        parser.add_argument('name', type=str, location='form')
        parser.add_argument('size', type=int, location='form')

        # These arguments have to be passed in the headers, otherwise it won't work
        parser.add_argument('X-File-Type', type=int, location='headers')
        parser.add_argument('X-Scan-Type', type=int, location='headers')
        parser.add_argument('X-Repository-ID', type=int, location='headers')
        parser.add_argument('Content-Type', type=str, location='headers')
        args = parser.parse_args()

        # Retrieve file and scan types for this file
        file_type_dao = FileTypeDao(self.db_session())
        file_type = file_type_dao.retrieve(id=args['X-File-Type'])
        scan_type_dao = ScanTypeDao(self.db_session())
        scan_type = scan_type_dao.retrieve(id=args['X-Scan-Type'])

        # Retrieve repository for this file
        repository_dao = RepositoryDao(self.db_session())
        repository = repository_dao.retrieve(id=args['X-Repository-ID'])

        # Set content type to something generic if it was not specified
        if args['Content-Type'] is None:
            args['Content-Type'] = 'application/octet-stream'

        # Create the file and return its dictionary info
        f_dao = FileDao(self.db_session())
        f = f_dao.create(
            name=args['name'], file_type=file_type, scan_type=scan_type, content_type=args['Content-Type'],
            size=args['size'], storage_id=args['id'], storage_path=args['path'], repository=repository)

        return f.to_dict(), http.CREATED_201


# ----------------------------------------------------------------------------------------------------------------------
class FileResource(BaseResource):

    URI = '/files/{}'

    @token_required
    def get(self, id):

        # Retrieve file meta data from the database
        f_dao = FileDao(self.db_session())
        f = f_dao.retrieve(id=id)

        # Return file meta information. To download the actual file contents use
        # the /file-contents/{} endpoint
        return f.to_dict(), http.OK_200


# ----------------------------------------------------------------------------------------------------------------------
class FileSetsResource(BaseResource):

    URI = '/file-sets'

    @token_required
    def get(self):

        # Get optional 'name' parameter if client is searching specific file set.
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='args')
        args = parser.parse_args()

        # Retrieve all file sets
        file_set_dao = FileSetDao(self.db_session())
        file_sets = file_set_dao.retrieve_all(**args)
        result = [file_set.to_dict() for file_set in file_sets]

        return result, http.OK_200

    @token_required
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        args = parser.parse_args()

        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.create(**args)

        return file_set.to_dict(), http.CREATED_201


# ----------------------------------------------------------------------------------------------------------------------
class FileSetResource(BaseResource):

    URI = '/file-sets/{}'

    @token_required
    def get(self, id):

        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.retrieve(id=id)

        return file_set.to_dict(), http.OK_200

    @token_required
    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        args = parser.parse_args()

        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.retrieve(id=id)
        file_set.name = args['name']
        file_set_dao.save(file_set)

        return file_set.to_dict(), http.OK_200

    @token_required
    def delete(self, id):

        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.retrieve(id=id)
        file_set_dao.delete(file_set)

        return {}, http.NO_CONTENT_204


# ----------------------------------------------------------------------------------------------------------------------
class FileSetFilesResource(BaseResource):

    URI = '/file-sets/{}/files'

    def get(self, id):

        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.retrieve(id=id)
        files = [f.to_dict() for f in file_set.files]

        return files, http.OK_200


# ----------------------------------------------------------------------------------------------------------------------
class FileSetFileResource(BaseResource):

    URI = '/file-sets/{}/files/{}'

    def put(self, id, file_id):

        # Get file set DAO and retrieve file in question
        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.retrieve(id=id)
        f_dao = FileDao(self.db_session())
        f = f_dao.retrieve(id=file_id)

        if f not in file_set.files:
            # Verify that given file complies with file set schema. This requires that
            # schema validation is enabled on the file set. The schema specification
            # specifies which additional arguments should be provided for each file, e.g.,
            # subject ID, session ID, etc.
            # TODO: Implement file set schemas or something similar...
            if file_set.schema_enabled:
                pass

            # Schema seems to be satisfied so add the file to the set and save.
            file_set.files.append(f)
            file_set_dao.save(file_set)

        return file_set.to_dict(), http.OK_200

    def delete(self, id, file_id):

        file_set_dao = FileSetDao(self.db_session())
        file_set = file_set_dao.retrieve(id=id)
        f_dao = FileDao(self.db_session())
        f = f_dao.retrieve(id=file_id)

        if f in file_set.files:
            file_set.remove(f)
            file_set_dao.save(file_set)

        return file_set.to_dict(), http.OK_200
