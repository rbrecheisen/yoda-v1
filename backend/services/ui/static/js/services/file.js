'use strict';

angular.module('services')

    .service('FileService', ['$http', 'Upload', 'TokenService', 'RepositoryService', 'environ',

        function($http, Upload, TokenService, RepositoryService, environ) {

            var filesUri = 'http://'
                + environ.UI_SERVICE_HOST + ':'
                + environ.UI_SERVICE_PORT + '/storage/repositories';

            var uploadsUri = 'http://'
                + environ.UI_SERVICE_HOST + ':'
                + environ.UI_SERVICE_PORT + '/storage/uploads';

            return {

                getAll: function(id) {
                    return $http({
                        method: 'GET',
                        url: filesUri + '/' + id + '/files',
                        headers: TokenService.header()
                    })
                },

                get: function(id, file_id) {
                    return $http({
                        method: 'GET',
                        url: filesUri + '/' + id + '/files/' + file_id,
                        headers: TokenService.header()
                    })
                },

                upload: function(id, file, file_type_id, scan_type_id) {

                    var headers = TokenService.header();
                    headers['X-Repository-ID'] = id;
                    headers['X-File-Type'] = file_type_id;
                    headers['X-Scan-Type'] = scan_type_id;
                    headers['Content-Disposition'] = 'attachment; filename=' + file.name;

                    return Upload.upload({
                        url: uploadsUri, data: {file: file},
                        headers: headers,
                        resumeSizeResponseReader: function(data) {
                            return data.content.split('/')[0].split('-')[1] + 1;
                        }
                    });
                },

                delete: function(id, file_id) {
                    return $http({
                        method: 'DELETE',
                        url: filesUri + '/' + id + '/files/' + file_id,
                        headers: TokenService.header()
                    });
                }
            }
        }]);