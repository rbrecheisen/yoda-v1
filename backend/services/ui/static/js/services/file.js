'use strict';

angular.module('services')

    .service('FileService', ['$http', 'TokenService', 'RepositoryService', 'environ',

        function($http, TokenService, RepositoryService, environ) {

            var filesUri = 'http://'
                + environ.UI_SERVICE_HOST + ':'
                + environ.UI_SERVICE_PORT + '/storage/repositories';

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
                }
            }
        }]);