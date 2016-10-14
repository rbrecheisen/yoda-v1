'use strict';

angular.module('services')

    .service('FileService', ['$http', 'Upload', 'TokenService', 'RepositoryService', 'environ',
    // .service('FileService', ['$http', 'TokenService', 'RepositoryService', 'environ',
        function($http, Upload, TokenService, RepositoryService, environ) {
        // function($http, TokenService, RepositoryService, environ) {
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
                    // The Upload module inserts a weird WebKitFormBoundary header inside the file contents
                    // if you use either 'Content-Disposition' or 'Content-Type'. Unfortunately, the
                    // nginx-big-upload library expects 'Content-Disposition' to extract the file name.
                    // I changed the request_processor.lua script to also accept a X-File-Name header
                    headers['X-File-Name'] = file.name;
                    headers['Content-Disposition'] = 'attachment; filename=' + file.name;
                    // headers['Content-Type'] = 'multipart/form-data';
                    headers['Content-Type'] = 'application/octet-stream';

                    // return Upload.upload({
                    //     url: uploadsUri,
                    //     data: {file: file},
                    //     headers: headers,
                    //     resumeSizeResponseReader: function(data) {
                    //         return data.content.split('/')[0].split('-')[1] + 1;
                    //     }
                    // });

                    // For some reason, the ng-file-upload library sends the whole FormData object over
                    // the line which causes the 'WebKitBoundary' header to be inserted into the file
                    // contents. If I just send the raw file object directly (as below) it works but then
                    // I won't have resumable uploads.

                    // https://github.com/aws/aws-sdk-js/issues/547

                    return $http({
                        method: 'POST',
                        url: uploadsUri,
                        data: file,
                        headers: headers
                    });
                },

                download: function(media_link) {
                    return $http({
                        method: 'GET',
                        url: media_link,
                        responseType: 'blob',
                        headers: TokenService.header()
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