'use strict';

angular.module('services')

    .service('ScanTypeService', ['$http', 'TokenService', 'environ',

        function($http, TokenService, environ) {

            var scanTypesUri = 'http://'
                + environ.UI_SERVICE_HOST + ':'
                + environ.UI_SERVICE_PORT + '/storage/scan-types';

            return {

                getAll: function() {
                    return $http({
                        method: 'GET',
                        url: scanTypesUri,
                        headers: TokenService.header()
                    })
                }
            }
        }]);