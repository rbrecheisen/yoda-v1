'use strict';

angular.module('services')

    .service('FileTypeService', ['$http', 'TokenService', 'environ',

        function($http, TokenService, environ) {

            var fileTypesUri = 'http://'
                + environ.UI_SERVICE_HOST + ':'
                + environ.UI_SERVICE_PORT + '/storage/file-types';

            return {

                getAll: function() {
                    return $http({
                        method: 'GET',
                        url: fileTypesUri,
                        headers: TokenService.header()
                    })
                }
            }
        }]);